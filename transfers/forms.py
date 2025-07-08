from django import forms
from .models import Transfer, Country, Currency, PaymentMethod

class QuickTransferForm(forms.Form):
    amount = forms.DecimalField(label="Montant", min_value=1, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant'}))
    from_country = forms.ModelChoiceField(label="Pays d'envoi", queryset=Country.objects.all(), empty_label="Pays de départ", widget=forms.Select(attrs={'class': 'form-control'}))
    to_country = forms.ModelChoiceField(label="Pays de destination", queryset=Country.objects.all(), empty_label="Pays de destination", widget=forms.Select(attrs={'class': 'form-control'}))
    payment_method = forms.ModelChoiceField(label="Méthode de paiement", queryset=PaymentMethod.objects.all(), empty_label="Méthode de paiement", widget=forms.Select(attrs={'class': 'form-control'}))

class TransferCalculatorForm(forms.Form):
    amount = forms.DecimalField(label="Montant", min_value=1, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant'}))
    from_currency = forms.ModelChoiceField(label="Devise d'envoi", queryset=Currency.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    to_currency = forms.ModelChoiceField(label="Devise de réception", queryset=Currency.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

from django.core.validators import RegexValidator

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = [
            'receiver_name', 'receiver_phone', 'receiver_email', 'amount',
            'from_country', 'to_country', 'from_currency', 'to_currency',
            'payment_method', 'notes'
        ]
        widgets = {
            'receiver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'from_country': forms.Select(attrs={'class': 'form-control'}),
            'to_country': forms.Select(attrs={'class': 'form-control'}),
            'from_currency': forms.Select(attrs={'class': 'form-control'}),
            'to_currency': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'receiver_name': 'Nom du destinataire',
            'receiver_phone': 'Téléphone du destinataire',
            'receiver_email': 'Email du destinataire',
            'amount': 'Montant',
            'from_country': 'Pays d\'origine',
            'to_country': 'Pays de destination',
            'from_currency': 'Devise d\'origine',
            'to_currency': 'Devise de destination',
            'payment_method': 'Méthode de paiement',
            'notes': 'Notes additionnelles (optionnel)',
        }

    # Validation personnalisée pour receiver_phone
    receiver_phone = forms.CharField(
        validators=[
            RegexValidator(
                r'^\+?\d{10,15}$',
                message='Entrez un numéro de téléphone valide avec le code pays (ex. +22377134567).'
            )
        ],
        required=True,
        help_text='Entrez un numéro avec le code pays (ex. +223 pour le Mali).'
    )


class TransferTrackingForm(forms.Form):
    reference = forms.CharField(
        label="Numéro de référence",
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: MC250611F4C8',
            'class': 'form-control'
        })
    )
