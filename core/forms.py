from django import forms
from .models import Transfer, User

class QuickTransferForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Montant')
    from_country = forms.CharField(max_length=100, label='Pays d\'envoi')
    to_country = forms.CharField(max_length=100, label='Pays de destination')
    payment_method = forms.ChoiceField(
        choices=[
            ('card', 'Carte de crédit/débit'),
            ('bank', 'Compte bancaire'),
            ('cash', 'Espèces'),
        ],
        label='Méthode de paiement'
    )
    from_currency = forms.ChoiceField(
        choices=[
            ('USD', 'USD (Dollar américain)'),
            ('XAF', 'XAF (Franc CFA BEAC)'),
            ('GNF', 'GNF (Franc guinéen)'),
            ('CAD', 'CAD (Dollar canadien)'),
            ('XOF', 'XOF (Franc CFA BCEAO)'),
            ('MAD', 'MAD (Dirham marocain)'),
            ('TND', 'TND (Dinar tunisien)'),
            ('EUR', 'EUR (Euro)'),
            ('CNY', 'CNY (Yuan chinois)'),
            ('JPY', 'JPY (Yen japonais)'),
            ('RUB', 'RUB (Rouble russe)'),
        ],
        label='Devise d\'envoi'
    )
    to_currency = forms.ChoiceField(
        choices=[
            ('USD', 'USD (Dollar américain)'),
            ('XAF', 'XAF (Franc CFA BEAC)'),
            ('GNF', 'GNF (Franc guinéen)'),
            ('CAD', 'CAD (Dollar canadien)'),
            ('XOF', 'XOF (Franc CFA BCEAO)'),
            ('MAD', 'MAD (Dirham marocain)'),
            ('TND', 'TND (Dinar tunisien)'),
            ('EUR', 'EUR (Euro)'),
            ('CNY', 'CNY (Yuan chinois)'),
            ('JPY', 'JPY (Yen japonais)'),
            ('RUB', 'RUB (Rouble russe)'),
        ],
        label='Devise de réception'
    )

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['receiver_name', 'receiver_phone', 'amount', 'from_currency', 'to_currency', 'from_country', 'to_country', 'payment_method', 'fees', 'exchange_rate', 'received_amount', 'tracking_number', 'status']

    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = 'Montant'
        self.fields['from_country'].label = 'Pays d\'envoi'
        self.fields['to_country'].label = 'Pays de destination'
        self.fields['payment_method'].label = 'Méthode de paiement'
        for field in ['from_currency', 'to_currency', 'from_country', 'to_country', 'payment_method']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TrackTransferForm(forms.Form):
    tracking_number = forms.CharField(max_length=10, label='Numéro de suivi')

class AgentSearchForm(forms.Form):
    country = forms.CharField(max_length=100, required=False, label='Pays')
    city = forms.CharField(max_length=100, required=False, label='Ville')

class SupportForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Sujet')
    message = forms.CharField(widget=forms.Textarea, label='Message')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']