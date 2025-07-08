from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transfer, Country, Currency, ExchangeRate, PaymentMethod, TransferFee
from .forms import QuickTransferForm, TransferForm, TransferTrackingForm, TransferCalculatorForm
from decimal import Decimal

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
    """Handle money transfer process"""
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.sender = request.user
            
            # Get currency for countries
            from_currency = Currency.objects.filter(code='FCFA').first()  # Default to FCFA
            to_currency = Currency.objects.filter(code='FCFA').first()    # Default to FCFA
            
            # Calculate fees
            fee = calculate_fees(
                transfer.amount, 
                transfer.from_country, 
                transfer.to_country, 
                transfer.payment_method
            )
            
            # Calculate exchange rate and received amount
            exchange_rate = get_exchange_rate(from_currency, to_currency)
            received_amount = transfer.amount * exchange_rate
            
            # Update transfer object
            transfer.fee = fee
            transfer.total = transfer.amount + fee
            transfer.from_currency = from_currency
            transfer.to_currency = to_currency
            transfer.exchange_rate = exchange_rate
            transfer.received_amount = received_amount
            
            transfer.save()
            
            messages.success(request, f'Votre transfert a été initié avec succès! Numéro de référence: {transfer.reference}')
            return redirect('transfer_detail', reference=transfer.reference)
    else:
        form = TransferForm()
    
    context = {
        'form': form,
        'title': 'Envoyer de l\'argent'
    }
    return render(request, 'transfers/transfer_form.html', context)

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
            reference = form.cleaned_data['reference']
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

def find_agents(request):
    """Find MaliCash agents"""
    countries = Country.objects.all()
    selected_country = None
    
    if request.method == 'GET' and 'country' in request.GET:
        country_id = request.GET.get('country')
        if country_id:
            selected_country = get_object_or_404(Country, id=country_id)
    
    context = {
        'countries': countries,
        'selected_country': selected_country,
        'title': 'Trouver un agent'
    }
    return render(request, 'transfers/find_agents.html', context)