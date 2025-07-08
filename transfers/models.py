from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    id = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name_plural = "Countries"

class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=11)
    
    def __str__(self):
        return f"{self.code} ({self.name})"
    
    class Meta:
        verbose_name_plural = "Currencies"

class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_rates')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_rates')
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code}: {self.rate}"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class TransferFee(models.Model):
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    max_amount = models.DecimalField(max_digits=20, decimal_places=2)
    fee_fixed = models.DecimalField(max_digits=20, decimal_places=2)
    fee_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    from_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='from_fees')
    to_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='to_fees')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.from_country.code} to {self.to_country.code}: {self.fee_fixed} + {self.fee_percentage}%"

class Transfer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('completed', 'Complété'),
        ('cancelled', 'Annulé'),
        ('failed', 'Échoué'),
    )
    
    reference = models.CharField(max_length=15, unique=True, default='')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers')
    sender_name = models.CharField(max_length=100, blank=True)
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    fee = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=2, default=1.0)
    received_amount = models.DecimalField(max_digits=20, decimal_places=2)
    from_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='sent_transfers')
    to_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='received_transfers')
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='sent_transfers')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='received_transfers')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transfer_type = models.CharField(max_length=50, default="Mobile Money")
    
    def __str__(self):
        return f"Transfer {self.reference}: {self.amount} {self.from_currency.code} to {self.receiver_name}"
    
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)
    
    def generate_reference(self):
        return f"MC{timezone.now().strftime('%y%m%d')}{uuid.uuid4().hex[:4].upper()}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=2)
    longitude = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country.name}"
    