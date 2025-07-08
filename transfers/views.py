from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transfer, Country, Currency, ExchangeRate, PaymentMethod, TransferFee, Agent
from .forms import QuickTransferForm, TransferForm, TransferTrackingForm, TransferCalculatorForm
from decimal import Decimal
from django.db.models import Q
from django.core.mail import send_mail
from twilio.rest import Client
from .decorators import agent_required
from django.urls import reverse
import uuid
import requests
from django.conf import settings

def calculate_fees(amount, from_country, to_country, payment_method):
    """Calculate transfer fees based on amount, countries and payment method"""
    try:
        # Find the appropriate fee structure
        fee_structure = TransferFee.objects.filter(
            from_country=from_country,
            to_country=to_country,
            payment_method=payment_method,
            min_amount__lte=amount,
            max_amount__gte=amount
        ).first()
        
        if fee_structure:
            fixed_fee = fee_structure.fee_fixed
            percentage_fee = (amount * fee_structure.fee_percentage) / 100
            total_fee = fixed_fee + percentage_fee
            return total_fee
        else:
            # Default fee if no specific structure found
            return Decimal('5.00')
    except Exception as e:
        print(f"Error calculating fees: {e}")
        return Decimal('5.00')  # Default fee on error

def get_exchange_rate(from_currency, to_currency):
    """Get exchange rate between two currencies"""
    try:
        rate = ExchangeRate.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency
        ).first()
        
        if rate:
            return rate.rate
        else:
            # If direct rate not found, try reverse and invert
            reverse_rate = ExchangeRate.objects.filter(
                from_currency=to_currency,
                to_currency=from_currency
            ).first()
            
            if reverse_rate:
                return Decimal('1') / reverse_rate.rate
            
            # Default rate if not found
            return Decimal('1.0')
    except Exception as e:
        print(f"Error getting exchange rate: {e}")
        return Decimal('1.0')  # Default rate on error
    
@login_required
def transfer_money(request):
    """Initiate a money transfer"""
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.sender = request.user
            transfer.tracking_number = str(uuid.uuid4())[:10].upper()
            transfer.status = 'PENDING'
            transfer.sender_name = request.user.get_full_name() or request.user.username

            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']
            if not from_currency or not to_currency:
                messages.error(request, "Veuillez sélectionner les devises d'envoi et de réception.")
                return render(request, 'transfers/transfer_form.html', {'form': form})
            transfer.from_currency_id = from_currency.id
            transfer.to_currency_id = to_currency.id

            # Calcul des frais
            transfer.fee = transfer.amount * Decimal('0.02')

            # Récupération du taux de change
            api_key = settings.EXCHANGE_RATE_API_KEY
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency.code}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    rate = data['conversion_rates'].get(to_currency.code, 1)
                    if rate == 1 and from_currency.code != to_currency.code:
                        messages.error(request, "Taux de change non disponible pour cette paire de devises.")
                        return render(request, 'transfers/transfer_form.html', {'form': form})
                    transfer.exchange_rate = Decimal(str(rate))
                else:
                    messages.error(request, f'Erreur API (code {response.status_code}): {response.text}')
                    return render(request, 'transfers/transfer_form.html', {'form': form})
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Erreur de connexion à l’API : {str(e)}')
                return render(request, 'transfers/transfer_form.html', {'form': form})

            # Calcul du montant reçu
            transfer.received_amount = (transfer.amount * transfer.exchange_rate) - transfer.fee

            # Calcul du total manquant
            transfer.total = transfer.amount + transfer.fee

            transfer.save()

            tracking_url = request.build_absolute_uri(
                reverse('track_transfer')  # Remplace 'track_transfer' par le nom de ta vue
            )

            # Email à l'expéditeur
            send_mail(
                'Confirmation de transfert - MaliCash',
                f'Votre transfert de {transfer.amount} {transfer.from_currency.code} a été initié. Référence : {transfer.reference}',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )

            # Email au destinataire
            if transfer.receiver_email:
                send_mail(
                    'Notification de transfert - MaliCash',
                    f'Vous avez reçu un transfert de {transfer.amount} {transfer.from_currency.code}. Référence : {transfer.reference}',
                    settings.EMAIL_HOST_USER,
                    [transfer.receiver_email],
                    fail_silently=False,
                )

            # SMS au destinataire
            if transfer.receiver_phone:
                try:
                    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    message = client.messages.create(
                        body=f'Vous avez reçu un transfert de {transfer.amount} {transfer.from_currency.code}. Référence : {transfer.reference}',
                        from_=settings.TWILIO_PHONE_NUMBER,
                        to=f'+{transfer.receiver_phone}'
                    )
                    print(f"SMS envoyé : {message.sid}")
                    messages.success(request, f"SMS envoyé avec succès au destinataire (SID: {message.sid}).")
                except Exception as e:
                    print(f"Erreur SMS : {str(e)}")
                    messages.error(request, f"Échec de l'envoi du SMS : {str(e)}")

            messages.success(request, f'Transfert initié avec succès ! Numéro de suivi : {transfer.tracking_number}')
            return redirect('transfer_history')
    else:
        form = TransferForm()

    return render(request, 'transfers/transfer_form.html', {'form': form, 'title': 'Envoyer de l\'argent'})

# @login_required
# def transfer_money(request):
#     """Initiate a money transfer"""
#     if request.method == 'POST':
#         form = TransferForm(request.POST)
#         if form.is_valid():
#             transfer = form.save(commit=False)
#             transfer.sender = request.user
#             transfer.tracking_number = str(uuid.uuid4())[:10].upper()
#             transfer.status = 'PENDING'
#             transfer.sender_name = request.user.get_full_name() or request.user.username

#             from_currency = form.cleaned_data['from_currency']
#             to_currency = form.cleaned_data['to_currency']
#             if not from_currency or not to_currency:
#                 messages.error(request, "Veuillez sélectionner les devises d'envoi et de réception.")
#                 return render(request, 'transfers/transfer_form.html', {'form': form})
#             transfer.from_currency_id = from_currency.id
#             transfer.to_currency_id = to_currency.id

#             # Calcul des frais
#             transfer.fee = transfer.amount * Decimal('0.02')

#             # Récupération du taux de change
#             api_key = settings.EXCHANGE_RATE_API_KEY
#             url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency.code}"
#             try:
#                 response = requests.get(url, timeout=5)
#                 if response.status_code == 200:
#                     data = response.json()
#                     rate = data['conversion_rates'].get(to_currency.code, 1)
#                     if rate == 1 and from_currency.code != to_currency.code:
#                         messages.error(request, "Taux de change non disponible pour cette paire de devises.")
#                         return render(request, 'transfers/transfer_form.html', {'form': form})
#                     transfer.exchange_rate = Decimal(str(rate))
#                 else:
#                     messages.error(request, f'Erreur API (code {response.status_code}): {response.text}')
#                     return render(request, 'transfers/transfer_form.html', {'form': form})
#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f'Erreur de connexion à l’API : {str(e)}')
#                 return render(request, 'transfers/transfer_form.html', {'form': form})

#             # Calcul du montant reçu
#             transfer.received_amount = (transfer.amount * transfer.exchange_rate) - transfer.fee

#             # ✅ Calcul du total manquant
#             transfer.total = transfer.amount + transfer.fee

#             transfer.save()

#             tracking_url = request.build_absolute_uri(
#                 reverse('track_transfer')  # Remplace 'track_transfer' par le nom de ta vue
#             )

#             send_mail(
#                 'Confirmation de transfert - MaliCash',
#                 f'Votre transfert de {transfer.amount} {transfer.from_currency.code} a été initié. Référence : {transfer.reference}',
#                 settings.EMAIL_HOST_USER,
#                 [request.user.email],
#                 fail_silently=False,
#             )

#             # Email au destinataire
#             if transfer.receiver_email:
#                 send_mail(
#                     'Notification de transfert - MaliCash',
#                     f'Vous avez reçu un transfert de {transfer.amount} {transfer.from_currency.code}. Référence : {transfer.reference}',
#                     settings.EMAIL_HOST_USER,
#                     [transfer.receiver_email],
#                     fail_silently=False,
#                 )

#             # SMS au destinataire
#             if transfer.receiver_phone:
#                 try:
#                     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#                     message = client.messages.create(
#                         body=f'Vous avez reçu un transfert de {transfer.amount} {transfer.from_currency.code}. Référence : {transfer.reference}',
#                         from_=settings.TWILIO_PHONE_NUMBER,
#                         to=f'+{transfer.receiver_phone}'
#                     )
#                     print(f"SMS envoyé : {message.sid}")
#                 except Exception as e:
#                     print(f"Erreur SMS : {str(e)}")

#             messages.success(request, f'Transfert initié avec succès ! Numéro de suivi : {transfer.tracking_number}')
#             return redirect('transfer_history')
#     else:
#         form = TransferForm()

#     return render(request, 'transfers/transfer_form.html', {'form': form, 'title': 'Envoyer de l\'argent'})

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transfer  # ← modèle de l’app transfert
from .serializers import TransferSerializer  # ← serializer de l’app transfert

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@agent_required
def terminer_transfert(request, reference):
    transfer = get_object_or_404(Transfer, reference=reference)

    if transfer.status != 'completed':
        transfer.status = 'completed'
        transfer.save()

        # Envoi d'email
        send_mail(
            subject='Transfert terminé - MaliCash',
            message=(
                f'Bonjour {transfer.sender.get_full_name()},\n\n'
                f'Le transfert avec la référence {transfer.reference} a bien été reçu par {transfer.receiver_name}.\n'
                f'Montant : {transfer.amount} {transfer.from_currency.code}\n\n'
                'Merci d\'utiliser MaliCash !'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[transfer.sender.email],
            fail_silently=False,
        )

        messages.success(request, 'Le transfert a été marqué comme terminé et un email a été envoyé.')

    return redirect('transfers:detail', reference=reference)



@login_required
def transfer_detail(request, reference):
    """Show transfer details"""
    transfer = get_object_or_404(Transfer, reference=reference)
    
    # Only allow sender to view their own transfers
    if transfer.sender != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à voir ce transfert.")
        return redirect('home')
    
    context = {
        'transfer': transfer,
        'title': f'Transfert {reference}'
    }
    return render(request, 'transfers/transfer_detail.html', context)

@login_required
def transfer_history(request):
    """Show user's transfer history"""
    transfers = Transfer.objects.filter(sender=request.user).order_by('-created_at')
    print(f"Transferts trouvés : {transfers.count()}")  # Débogage
    
    context = {
        'transfers': transfers,
        'title': 'Historique des transferts'
    }
    return render(request, 'transfers/transfer_history.html', context)

def track_transfer(request):
    """Track a transfer by reference number"""
    transfer = None

    if request.method == 'POST':
        form = TransferTrackingForm(request.POST)
        if form.is_valid():
            reference = form.cleaned_data['reference'].strip().upper()

            if len(reference) < 12:
                messages.error(request, "Veuillez entrer une référence complète (ex: MC250611F4C8).")
            else:
                transfer = Transfer.objects.filter(reference=reference).first()
                if not transfer:
                    messages.error(request, f'Aucun transfert trouvé avec la référence {reference}')
    else:
        form = TransferTrackingForm()

    context = {
        'form': form,
        'transfer': transfer,
        'title': 'Suivi de transfert'
    }
    return render(request, 'transfers/track_transfer.html', context)


def calculator(request):
    """Calculate transfer amounts and fees"""
    result = None
    
    if request.method == 'POST':
        form = TransferCalculatorForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']
            
            # Get exchange rate
            exchange_rate = get_exchange_rate(from_currency, to_currency)
            
            # Calculate fee (2% for demo purposes)
            fee = amount * Decimal('0.02')
            
            # Calculate received amount
            converted_amount = amount * exchange_rate
            received_amount = converted_amount - fee
            
            result = {
                'amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'exchange_rate': exchange_rate,
                'fee': fee,
                'converted_amount': converted_amount,
                'received_amount': received_amount
            }
    else:
        form = TransferCalculatorForm()
    
    context = {
        'form': form,
        'result': result,
        'title': 'Calculateur de transfert'
    }
    return render(request, 'transfers/calculator.html', context)

# views.py
def agents_page(request):
    """Display agents page with services"""
    return render(request, 'transfers/agents.html')


# def agents(request):
#     agents = [
#         {
#             'nom': 'Boubou Camara',
#             'poste': 'Agent de communication',
#             'email': 'diawaradg53@gmail.com',
#             'tel': '+22390328598',
#             'photo': 'img/agents/boubou.jpg',
#         },
#         {
#             'nom': 'Fatoumata Diallo',
#             'poste': 'Agent de sécurité',
#             'email': 'fatou@malicash.ml',
#             'tel': '+22391234567',
#             'photo': 'img/agents/fatou.jpg',
#         },
#         {
#             'nom': 'Mamadou Konaté',
#             'poste': 'Agent de nettoyage',
#             'email': 'mamadou@malicash.ml',
#             'tel': '+22397876543',
#             'photo': 'img/agents/mamadou.jpg',
#         },
#         {
#             'nom': 'Aïssata Keïta',
#             'poste': 'Agent de livraison',
#             'email': 'livraison@malicash.ml',
#             'tel': '+22390112233',
#             'photo': 'img/agents/aissata.jpg',
#         },
#     ]
#     return render(request, 'core/agents.html', {'agents': agents})


# def find_agents(request):
#     """Find MaliCash agents"""
#     countries = Country.objects.all()
#     agents = Agent.objects.filter(is_active=True)
    
#     # Filter by country code
#     country_code = request.GET.get('country')
#     if country_code:
#         country = Country.objects.filter(code=country_code).first()
#         if country:
#             agents = agents.filter(country=country)
#             selected_country = country
#         else:
#             selected_country = None
#     else:
#         selected_country = None
    
#     # Filter by city
#     city = request.GET.get('city')
#     if city:
#         agents = agents.filter(city__icontains=city)
    
#     context = {
#         'countries': countries,
#         'agents': agents,
#         'selected_country': selected_country,
#         'title': 'Trouver un agent'
#     }
#     return render(request, 'transfers/find_agents.html', context)