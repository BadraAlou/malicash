from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import activate, get_language
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuickTransferForm, TransferForm, TrackTransferForm, AgentSearchForm, SupportForm, ProfileForm
from .models import Testimonial, FAQCategory, FAQ, Transfer, Agent, Currency, Notification, Referral
from transfers.models import Country
from django.core.mail import send_mail
import uuid
from decimal import Decimal
import requests  # Pour les taux de change via une API (optionnel)

def home(request):
    """Home page view"""
    if request.GET.get('language'):
        activate(request.GET.get('language'))
    quick_form = QuickTransferForm()
    testimonials = Testimonial.objects.filter(active=True)
    
    currencies = [
        {"countries": "États-Unis", "currency": "USD (Dollar américain)", "flag": "us"},
        {"countries": "Gabon, Cameroun, Guinée Équatoriale", "currency": "XAF (Franc CFA BEAC)", "flag": "ga"},
        {"countries": "Guinée", "currency": "GNF (Franc guinéen)", "flag": "gn"},
        {"countries": "Canada", "currency": "CAD (Dollar canadien)", "flag": "ca"},
        {"countries": "Burkina Faso, Bénin, Niger, Togo", "currency": "XOF (Franc CFA BCEAO)", "flag": "bf"},
        {"countries": "Maroc", "currency": "MAD (Dirham marocain)", "flag": "ma"},
        {"countries": "Tunisie", "currency": "TND (Dinar tunisien)", "flag": "tn"},
        {"countries": "Espagne", "currency": "EUR (Euro)", "flag": "es"},
        {"countries": "Chine", "currency": "CNY (Yuan chinois)", "flag": "cn"},
        {"countries": "Japon", "currency": "JPY (Yen japonais)", "flag": "jp"},
        {"countries": "Russie", "currency": "RUB (Rouble russe)", "flag": "ru"},
    ]

    context = {
        'quick_form': quick_form,
        'testimonials': testimonials,
        'currencies': currencies,
        'title': 'Accueil'
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    context = {
        'title': 'À propos'
    }
    return render(request, 'core/about.html', context)

def services(request):
    """Services page view"""
    context = {
        'title': 'Nos Services'
    }
    return render(request, 'core/services.html', context)

def faq(request):
    """FAQ page view"""
    categories = FAQCategory.objects.all()
    faqs = FAQ.objects.all().order_by('category', 'order')
    
    context = {
        'categories': categories,
        'faqs': faqs,
        'title': 'Questions fréquentes'
    }
    return render(request, 'core/faq.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validation basique
        if not all([name, email, subject, message]):
            messages.error(request, 'Tous les champs sont obligatoires.')
            return render(request, 'core/contact.html')
        
        try:
            # Envoyer l'email
            full_message = f"""
            Nouveau message de contact depuis le site MaliCash:
            
            Nom: {name}
            Email: {email}
            Sujet: {subject}
            
            Message:
            {message}
            """
            
            send_mail(
                subject=f'[MaliCash Contact] {subject}',
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['contactmalicash@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.')
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, 'Une erreur est survenue lors de l\'envoi du message. Veuillez réessayer.')
    
    return render(request, 'core/contact.html')


# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.urls import reverse
# from django.utils import timezone
# from django.views.decorators.csrf import csrf_protect
# from twilio.rest import Client
# from transfers.models import Transfer, Country, Currency, PaymentMethod
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
# from core.utils import send_transfer_email, send_sms


# @csrf_protect
# def process_mobile_transfer(request):
#     if request.method == "POST":
#         recipient_number = request.POST.get("recipient_number")
#         amount = request.POST.get("amount")

#         if not recipient_number or not amount:
#             messages.error(request, "Veuillez remplir tous les champs.")
#             return redirect(reverse("home"))

#         if not recipient_number.startswith("+223") or len(recipient_number) < 10:
#             messages.error(request, "Numéro de mobile invalide. Utilisez le format +223XXXXXXXX.")
#             return redirect(reverse("home"))

#         try:
#             amount = float(amount)
#             if amount <= 0:
#                 messages.error(request, "Le montant doit être positif.")
#                 return redirect(reverse("home"))
#         except ValueError:
#             messages.error(request, "Montant invalide.")
#             return redirect(reverse("home"))

#         initial_amount = amount
#         fee = round(amount * 0.02, 2)
#         amount_after_fee = amount - fee
#         total = amount
#         received_amount = amount_after_fee

#         try:
#             from_country = Country.objects.get(id=1)
#             to_country = Country.objects.get(id=1)
#             from_currency = Currency.objects.get(id=1)
#             to_currency = Currency.objects.get(id=1)
#             payment_method = PaymentMethod.objects.get(id=1)
#         except ObjectDoesNotExist:
#             messages.error(request, "Les données de configuration sont manquantes.")
#             return redirect(reverse("transfer_history"))

#         # Vérifie les permissions
#         if not request.user.has_perm('transfers.can_process_mobile_money'):
#             messages.warning(request, "Votre transfert est en cours, en attente de confirmation de l'admin.")
#             return redirect(reverse("transfer_history"))

#         # Enregistrement du transfert
#         transfer = Transfer.objects.create(
#             sender=request.user,
#             sender_name=request.user.get_full_name() or request.user.username,
#             receiver_name=recipient_number,
#             receiver_phone=recipient_number,
#             amount=amount_after_fee,
#             fee=fee,
#             total=total,
#             received_amount=received_amount,
#             from_country=from_country,
#             to_country=to_country,
#             from_currency=from_currency,
#             to_currency=to_currency,
#             payment_method=payment_method,
#             status="pending",
#             transfer_type="Mobile Money"
#         )

#         # ✉️ Envoi d'email à l'expéditeur
#         send_transfer_email(
#             to_email=request.user.email,
#             subject="Confirmation de transfert Mobile Money - MaliCash",
#             message=f"Votre transfert de {initial_amount} XOF a été initié.\nRéférence : {transfer.reference}."
#         )

#         # 📲 Envoi de SMS au destinataire
#         sms_body = f'Vous avez un transfert de {initial_amount} XOF. Réf: {transfer.reference} (Frais: {fee} XOF).'
#         sms_ok, sms_info = send_sms(recipient_number, sms_body)
#         if sms_ok:
#             messages.success(request, f"SMS envoyé avec succès (SID: {sms_info})")
#         else:
#             messages.error(request, f"Échec de l'envoi du SMS : {sms_info}")

#         messages.success(request, f'Transfert soumis ! Référence : {transfer.reference}')
#         return redirect(reverse("transfer_history"))

#     return redirect(reverse("home"))
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from twilio.rest import Client
from transfers.models import Transfer, Country, Currency, PaymentMethod
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


# Configuration Twilio (à ajouter dans settings.py)
# TWILIO_ACCOUNT_SID = 'votre_sid_ici'
# TWILIO_AUTH_TOKEN = 'votre_token_ici'
# TWILIO_PHONE_NUMBER = '+1234567890'

@csrf_protect
def process_mobile_transfer(request):
    if request.method == "POST":
        recipient_number = request.POST.get("recipient_number")
        amount = request.POST.get("amount")

        if not recipient_number or not amount:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect(reverse("home"))

        if not recipient_number.startswith("+223") or len(recipient_number) < 10:
            messages.error(request, "Numéro de mobile invalide. Utilisez le format +223XXXXXXXX.")
            return redirect(reverse("home"))

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Le montant doit être positif.")
                return redirect(reverse("home"))
        except ValueError:
            messages.error(request, "Montant invalide.")
            return redirect(reverse("home"))

        initial_amount = amount
        fee = amount * 0.02
        amount_after_fee = amount - fee
        total = amount
        received_amount = amount_after_fee

        try:
            from_country = Country.objects.get(id=1)
            to_country = Country.objects.get(id=1)
            from_currency = Currency.objects.get(id=1)
            to_currency = Currency.objects.get(id=1)
            payment_method = PaymentMethod.objects.get(id=1)  # Assumé pour Mobile Money
        except ObjectDoesNotExist:
            messages.error(request, "Les données de configuration sont manquantes.")
            return redirect(reverse("transfer_history"))

        if not request.user.has_perm('transfers.can_process_mobile_money'):
            messages.warning(request, "Votre transfert est en cours, on attend juste la confirmation de l'admin.")
            return redirect(reverse("transfer_history"))

        transfer = Transfer(
            sender=request.user,
            sender_name=request.user.get_full_name() or request.user.username,
            receiver_name=recipient_number,
            receiver_phone=recipient_number,
            amount=amount_after_fee,
            fee=fee,
            total=total,
            received_amount=received_amount,
            from_country=from_country,
            to_country=to_country,
            from_currency=from_currency,
            to_currency=to_currency,
            payment_method=payment_method,
            status="pending",
            transfer_type="Mobile Money"
        )
        transfer.save()
        print(f"Transfert sauvegardé - ID: {transfer.id}, Référence: {transfer.reference}")  # Débogage

        # Envoi de SMS
        if recipient_number:
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Votre transfert de {initial_amount} XOF (Réf: {transfer.reference}) est en attente. Frais: {fee} XOF.',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=recipient_number
                )
                print(f"SMS envoyé : {message.sid}")
                messages.success(request, f"Transfert soumis ! Référence : {transfer.reference}. SMS envoyé (SID: {message.sid}).")
            except Exception as e:
                print(f"Erreur SMS : {str(e)}")
                messages.success(request, f"Transfert soumis ! Référence : {transfer.reference}. Échec SMS : {str(e)}")

        # Redirection vers l'historique
        return redirect(reverse("transfer_history"))

    return redirect(reverse("home"))

# Configuration Twilio (à ajouter dans settings.py)
# TWILIO_ACCOUNT_SID = 'votre_sid_ici'
# TWILIO_AUTH_TOKEN = 'votre_token_ici'
# TWILIO_PHONE_NUMBER = '+1234567890'

# @csrf_protect
# def process_mobile_transfer(request):
#     countries = Country.objects.all()  # Tous les pays
#     currencies = Currency.objects.all()  # Toutes les devises

#     if request.method == "POST":
#         recipient_number = request.POST.get("recipient_number")
#         amount = request.POST.get("amount")
#         from_country_id = request.POST.get("from_country")  # ID du pays d'origine
#         to_country_id = request.POST.get("to_country")     # ID du pays de destination
#         from_currency_id = request.POST.get("from_currency")  # ID de la devise d'origine
#         to_currency_id = request.POST.get("to_currency")     # ID de la devise de destination

#         if not recipient_number or not amount or not from_country_id or not to_country_id or not from_currency_id or not to_currency_id:
#             messages.error(request, "Veuillez remplir tous les champs.")
#             return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})

#         if not recipient_number.startswith("+223") or len(recipient_number) < 10:
#             messages.error(request, "Numéro de mobile invalide. Utilisez le format +223XXXXXXXX.")
#             return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})

#         try:
#             amount = float(amount)
#             if amount <= 0:
#                 messages.error(request, "Le montant doit être positif.")
#                 return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})
#         except ValueError:
#             messages.error(request, "Montant invalide.")
#             return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})

#         initial_amount = amount
#         fee = amount * 0.02
#         amount_after_fee = amount - fee
#         total = amount
#         received_amount = amount_after_fee

#         try:
#             from_country = Country.objects.get(id=from_country_id)
#             to_country = Country.objects.get(id=to_country_id)
#             from_currency = Currency.objects.get(id=from_currency_id)
#             to_currency = Currency.objects.get(id=to_currency_id)
#             payment_method = PaymentMethod.objects.get(id=1)  # Toujours 1 pour Mobile Money
#         except ObjectDoesNotExist:
#             messages.error(request, "Les données de configuration sont manquantes.")
#             return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})

#         if not request.user.has_perm('transfers.can_process_mobile_money'):
#             messages.warning(request, "Votre transfert est en cours, on attend juste la confirmation de l'admin.")
#             return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})

#         transfer = Transfer(
#             sender=request.user,
#             sender_name=request.user.get_full_name() or request.user.username,
#             receiver_name=recipient_number,
#             receiver_phone=recipient_number,
#             amount=amount_after_fee,
#             fee=fee,
#             total=total,
#             received_amount=received_amount,
#             from_country=from_country,
#             to_country=to_country,
#             from_currency=from_currency,
#             to_currency=to_currency,
#             payment_method=payment_method,
#             status="pending",
#             transfer_type="Mobile Money"
#         )
#         transfer.save()
#         print(f"Transfert sauvegardé - ID: {transfer.id}, Référence: {transfer.reference}")

#         if recipient_number:
#             try:
#                 client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#                 message = client.messages.create(
#                     body=f'Votre transfert de {initial_amount} XOF (Réf: {transfer.reference}) est en attente. Frais: {fee} XOF.',
#                     from_=settings.TWILIO_PHONE_NUMBER,
#                     to=recipient_number
#                 )
#                 print(f"SMS envoyé : {message.sid}")
#                 messages.success(request, f"SMS envoyé (SID: {message.sid}).")
#             except Exception as e:
#                 print(f"Erreur SMS : {str(e)}")
#                 messages.error(request, f"Échec SMS : {str(e)}")

#         messages.success(request, f'Transfert soumis ! Référence : {transfer.reference}. En attente de confirmation.')
#         return redirect(reverse("transfer_history"))

#     return render(request, 'transfers/transfer_form.html', {'countries': countries, 'currencies': currencies})

# Configuration Twilio (à ajouter dans settings.py)
# TWILIO_ACCOUNT_SID = 'votre_sid_ici'
# TWILIO_AUTH_TOKEN = 'votre_token_ici'
# TWILIO_PHONE_NUMBER = '+1234567890'

# @csrf_protect
# def process_mobile_transfer(request):
#     if request.method == "POST":
#         recipient_number = request.POST.get("recipient_number")
#         amount = request.POST.get("amount")

#         if not recipient_number or not amount:
#             messages.error(request, "Veuillez remplir tous les champs.")
#             return redirect(reverse("home"))

#         if not recipient_number.startswith("+223") or len(recipient_number) < 10:
#             messages.error(request, "Numéro de mobile invalide. Utilisez le format +223XXXXXXXX.")
#             return redirect(reverse("home"))

#         try:
#             amount = float(amount)
#             if amount <= 0:
#                 messages.error(request, "Le montant doit être positif.")
#                 return redirect(reverse("home"))
#         except ValueError:
#             messages.error(request, "Montant invalide.")
#             return redirect(reverse("home"))

#         initial_amount = amount
#         fee = amount * 0.02
#         amount_after_fee = amount - fee
#         total = amount
#         received_amount = amount_after_fee

#         try:
#             from_country = Country.objects.get(id=1)
#             to_country = Country.objects.get(id=1)
#             from_currency = Currency.objects.get(id=1)
#             to_currency = Currency.objects.get(id=1)
#             payment_method = PaymentMethod.objects.get(id=1)
#         except ObjectDoesNotExist:
#             messages.error(request, "Les données de configuration sont manquantes.")
#             return redirect(reverse("transfer_history"))

#         # Vérification manuelle de la permission
#         if not request.user.has_perm('transfers.can_process_mobile_money'):
#             messages.warning(request, "Votre transfert est en cours, on attend juste la confirmation de l'admin.")
#             return redirect(reverse("transfer_history"))

#         transfer = Transfer(
#             sender=request.user,
#             sender_name=request.user.get_full_name() or request.user.username,
#             receiver_name=recipient_number,
#             receiver_phone=recipient_number,
#             amount=amount_after_fee,
#             fee=fee,
#             total=total,
#             received_amount=received_amount,
#             from_country=from_country,
#             to_country=to_country,
#             from_currency=from_currency,
#             to_currency=to_currency,
#             payment_method=payment_method,
#             status="pending",
#             transfer_type="Mobile Money"
#         )
#         transfer.save()
#         print(f"Transfert sauvegardé - ID: {transfer.id}, Référence: {transfer.reference}")  # Débogage

#         # Envoi de SMS (séparé pour éviter d'interrompre la sauvegarde)
#         if recipient_number:
#             try:
#                 client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#                 message = client.messages.create(
#                     body=f'Votre transfert de {initial_amount} XOF (Réf: {transfer.reference}) est en attente. Frais: {fee} XOF.',
#                     from_=settings.TWILIO_PHONE_NUMBER,
#                     to=recipient_number
#                 )
#                 print(f"SMS envoyé : {message.sid}")
#                 messages.success(request, f"SMS envoyé (SID: {message.sid}).")
#             except Exception as e:
#                 print(f"Erreur SMS : {str(e)}")
#                 messages.error(request, f"Échec SMS : {str(e)}")

#         messages.success(request, f'Transfert soumis ! Référence : {transfer.reference}. En attente de confirmation.')
#         return redirect(reverse("transfer_history"))

#     return redirect(reverse("home"))

@csrf_protect
@login_required
#@permission_required('transfers.can_approve_mobile_money', raise_exception=True)
def approve_transfer(request, reference):
    if request.method == "POST" and request.user.is_staff:
        transfer = get_object_or_404(Transfer, reference=reference, status="pending")
        if transfer.transfer_type != "Mobile Money":
            messages.error(request, "Vous n'êtes autorisé à approuver que les transferts Mobile Money.")
            return redirect(reverse("transfer_history"))
        transfer.status = "success"
        transfer.save()
        recipient_number = transfer.receiver_phone
        amount = transfer.received_amount
        fee = transfer.fee
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Votre transfert de {amount} XOF (Réf: {transfer.reference}) a été approuvé. L\'argent a été envoyé. Frais: {fee:.2f} XOF.',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=recipient_number
            )
            print(f"SMS d'approbation : {message.sid}")
            messages.success(request, f"Approuvé et SMS envoyé (SID: {message.sid}).")
            # Notification à l'utilisateur connecté (expéditeur)
            messages.success(request, f"Le transfert {transfer.reference} a été approuvé et l'argent envoyé.")
        except Exception as e:
            print(f"Erreur SMS : {str(e)}")
            messages.error(request, f"Échec SMS d'approbation : {str(e)}")
        return redirect(reverse("transfer_history"))
    return redirect(reverse("transfer_history"))

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from transfers.models import Transfer, PaymentMethod
# from core.models import  Currency
# from transfers.models import Country
# from decimal import Decimal

# @login_required
# def effectuer_transfers_mobile(request):
#     if request.method == 'POST':
#         numero = request.POST.get('numero')
#         montant = request.POST.get('montant')

#         # Objets liés obligatoires
#         from_country = Country.objects.first()
#         to_country = Country.objects.first()
#         from_currency = Currency.objects.first()
#         to_currency = Currency.objects.first()
#         payment_method = PaymentMethod.objects.first()

#         fee = 0  # adapte selon ta logique
#         total = float(montant) + fee
#         exchange_rate = 1
#         received_amount = float(montant)

#         try:
#             transfer = Transfer.objects.create(
#                 sender=request.user,
#                 sender_name=request.user.get_full_name() or "Inconnu",
#                 receiver_name="Nom inconnu",
#                 receiver_phone=numero,
#                 amount=montant,
#                 fee=fee,
#                 total=total,
#                 exchange_rate=exchange_rate,
#                 received_amount=received_amount,
#                 from_country=from_country,
#                 to_country=to_country,
#                 from_currency=from_currency,
#                 to_currency=to_currency,
#                 payment_method=payment_method,
#                 status="pending",
#                 transfer_type="Mobile Money"
#             )
#             print("Transfert créé avec succès :", transfer)
#         except Exception as e:
#             print("Erreur lors de la création du transfert :", e)
#             # Optionnel : tu peux aussi gérer un message d'erreur à afficher à l'utilisateur ici

#         return redirect('transfer_history')

#     return redirect('services')


# ****************** Problème debut

# from transfers.models import Country, Currency, PaymentMethod

# country, created = Country.objects.update_or_create(
#     id=1,
#     defaults={'name': 'Mali', 'code': 'MLI'}
# )
# print(f"Country mis à jour/créé: {created}, ID: {country.id}")

# currency, created = Currency.objects.update_or_create(
#     id=1,
#     defaults={'code': 'XOF', 'name': 'Franc CFA'}
# )
# print(f"Currency mis à jour/créé: {created}, ID: {currency.id}")

# payment_method, created = PaymentMethod.objects.update_or_create(
#     id=1,
#     defaults={'name': 'Mobile Money'}
# )
# print(f"PaymentMethod mis à jour/créé: {created}, ID: {payment_method.id}")

# ****************** Problème fin


def home(request):
    context = {
        'transfers': request.session.get('transfers', [])
    }
    return render(request, 'core/home.html', context)

# Vue pour l'approbation par l'admin (exemple, à sécuriser)
# @csrf_protect
# def approve_transfer(request, reference):
#     if request.method == "POST" and request.user.is_staff:  # Vérifie si l'utilisateur est admin
#         transfers = request.session.get('transfers', [])
#         for transfer in transfers:
#             if transfer["reference"] == reference and transfer["status"] == "pending":
#                 transfer["status"] = "success"
#                 recipient_number = transfer["receiver_name"]
#                 amount = transfer["amount"]
#                 try:
#                     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#                     message = client.messages.create(
#                         body=f'Votre transfert de {amount} XOF (Réf: {reference}) a été approuvé. Frais: {transfer["fee"]} XOF.',
#                         from_=settings.TWILIO_PHONE_NUMBER,
#                         to=recipient_number
#                     )
#                     print(f"SMS d'approbation envoyé : {message.sid}")
#                     messages.success(request, f"Transfert approuvé et SMS envoyé (SID: {message.sid}).")
#                 except Exception as e:
#                     print(f"Erreur SMS d'approbation : {str(e)}")
#                     messages.error(request, f"Échec de l'envoi du SMS d'approbation : {str(e)}")
#                 break
#         request.session.modified = True
#     return redirect(reverse("home"))

def terms(request):
    """Terms and conditions page view"""
    context = {
        'title': 'Conditions d\'utilisation'
    }
    return render(request, 'core/terms.html', context)

def privacy(request):
    """Privacy policy page view"""
    context = {
        'title': 'Politique de confidentialité'
    }
    return render(request, 'core/privacy.html', context)

# Nouvelle vue : Transfert d'argent
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

            # Affectation manuelle des devises
            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']
            transfer.from_currency = from_currency
            transfer.to_currency = to_currency

            # Calcul des frais
            transfer.fees = transfer.amount * Decimal('0.02')

            # Taux de change simulé
            exchange_rates = {
                'USD': {'XAF': 600, 'GNF': 9000, 'CAD': 1.35, 'XOF': 600, 'MAD': 10, 'TND': 3.1, 'EUR': 0.92, 'CNY': 7.1, 'JPY': 150, 'RUB': 90},
                'XAF': {'USD': 0.0017},
            }
            rate = exchange_rates.get(str(from_currency), {}).get(str(to_currency), 1)
            transfer.exchange_rate = Decimal(rate)
            transfer.received_amount = (transfer.amount * transfer.exchange_rate) - transfer.fees

            transfer.save()

            # Notification
            Notification.objects.create(
                user=request.user,
                message=f"Votre transfert de {transfer.amount} {transfer.from_currency} vers {transfer.to_country} a été initié. Numéro de suivi : {transfer.tracking_number}"
            )

            # Email
            send_mail(
                'Confirmation de transfert - MaliCash',
                f'Votre transfert a été initié avec succès. Numéro de suivi : {transfer.tracking_number}',
                'noreply@malicash.com',
                [request.user.email],
                fail_silently=True,
            )

            messages.success(request, f'Transfert initié avec succès ! Numéro de suivi : {transfer.tracking_number}')
            return redirect('transfer_history')
    else:
        form = TransferForm()

    context = {
        'form': form,
        'title': 'Envoyer de l\'argent'
    }
    return render(request, 'core/transfer_money.html', context)


# Nouvelle vue : Suivi de transfert
def track_transfer(request):
    """Track a money transfer"""
    form = TrackTransferForm(request.GET or None)
    transfer = None
    if form.is_valid():
        tracking_number = form.cleaned_data['tracking_number']
        transfer = get_object_or_404(Transfer, tracking_number=tracking_number)
    
    context = {
        'form': form,
        'transfer': transfer,
        'title': 'Suivi de transfert'
    }
    return render(request, 'core/track_transfer.html', context)

# Nouvelle vue : Calculateur de frais et taux
def calculator(request):
    """Currency converter and fee calculator"""
    amount = request.GET.get('amount', 0)
    from_currency = request.GET.get('from_currency', 'USD')
    to_currency = request.GET.get('to_currency', 'XAF')
    
    # Taux de change simulé (peut être remplacé par une API réelle)
    exchange_rates = {
        'USD': {'XAF': 600, 'GNF': 9000, 'CAD': 1.35, 'XOF': 600, 'MAD': 10, 'TND': 3.1, 'EUR': 0.92, 'CNY': 7.1, 'JPY': 150, 'RUB': 90},
        'XAF': {'USD': 0.0017},
        # Ajoute d'autres taux selon besoin
    }
    
    # Calcul
    try:
        amount = Decimal(amount)
        rate = Decimal(exchange_rates.get(from_currency, {}).get(to_currency, 1))
        fees = amount * Decimal('0.02')  # Frais de 2%
        received_amount = (amount * rate) - fees
    except:
        amount = 0
        fees = 0
        received_amount = 0
        rate = 1
    
    context = {
        'amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'fees': fees,
        'received_amount': received_amount,
        'exchange_rate': rate,
        'title': 'Calculateur de frais'
    }
    return render(request, 'core/calculator.html', context)

# def local_agents(request):
#     """Affiche les agents internes de l'agence de Bacodjicoroni"""
#     agents = [
#         {
#             'name': 'Boubou Camara',
#             'role': 'Agent de communication',
#             'email': 'diawaradg53@gmail.com',
#             'phone': '+22390328598'
#         },
#         {
#             'name': 'Fatoumata Diallo',
#             'role': 'Agent de sécurité',
#             'email': 'fatou@malicash.ml',
#             'phone': '+22391234567'
#         },
#         {
#             'name': 'Mamadou Konaté',
#             'role': 'Agent de nettoyage',
#             'email': 'mamadou@malicash.ml',
#             'phone': '+22397876543'
#         },
#         {
#             'name': 'Aïssata Keïta',
#             'role': 'Agent de livraison',
#             'email': 'livraison@malicash.ml',
#             'phone': '+22390112233'
#         }
#     ]

#     context = {
#         'agents': agents,
#         'title': 'Nos agents à Bacodjicoroni'
#     }
#     return render(request, 'core/local_agents.html', context)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Testimonial, FAQCategory, FAQ, Transfer, Agent, Currency,
    Notification, Referral
)
from .serializers import (
    TestimonialSerializer, FAQCategorySerializer, FAQSerializer,
    TransferSerializer, AgentSerializer, CurrencySerializer,
    NotificationSerializer, ReferralSerializer
)

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class FAQCategoryViewSet(viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

@login_required
def transfer_history(request):
    """View transfer history for the logged-in user"""
    transfers = Transfer.objects.filter(sender=request.user).order_by('-created_at')
    
    context = {
        'transfers': transfers,
        'title': 'Historique des transferts'
    }
    return render(request, 'core/transfer_history.html', context)

# Nouvelle vue : Profil utilisateur
@login_required
def profile(request):
    """View and edit user profile"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Mon profil'
    }
    return render(request, 'core/profile.html', context)

# Nouvelle vue : Support client
@login_required
def support(request):
    """Submit a support request"""
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            # Envoie un email au support (simulé ici)
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                f'Demande de support : {subject}',
                message,
                request.user.email,
                ['support@malicash.com'],
                fail_silently=True,
            )
            messages.success(request, 'Votre demande a été envoyée avec succès !')
            return redirect('support')
    else:
        form = SupportForm()
    
    context = {
        'form': form,
        'title': 'Support client'
    }
    return render(request, 'core/support.html', context)

# Nouvelle vue : Programme de parrainage/récompenses
@login_required
def referral(request):
    """Referral program view"""
    referral_code = request.user.referral_code if hasattr(request.user, 'referral_code') else None
    referrals = Referral.objects.filter(referrer=request.user)
    
    if not referral_code:
        # Générer un code de parrainage unique si l'utilisateur n'en a pas
        request.user.referral_code = str(uuid.uuid4())[:8].upper()
        request.user.save()
        referral_code = request.user.referral_code
    
    context = {
        'referral_code': referral_code,
        'referrals': referrals,
        'title': 'Programme de parrainage'
    }
    return render(request, 'core/referral.html', context)

# Nouvelle vue : Notifications
@login_required
def notifications(request):
    """View user notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Marquer les notifications comme lues
    if request.GET.get('mark_read'):
        notifications.update(is_read=True)
        messages.success(request, 'Notifications marquées comme lues.')
        return redirect('notifications')
    
    context = {
        'notifications': notifications,
        'title': 'Notifications'
    }
    return render(request, 'core/notifications.html', context)

