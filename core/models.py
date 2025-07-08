from django.db import models
from django.contrib.auth.models import User
import uuid

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    comment = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.location}"

class FAQCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.question

class Transfer(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('COMPLETED', 'Complété'),
        ('FAILED', 'Échoué'),
    ]
    COUNTRY_CHOICES = [
        ('', 'Sélectionnez un pays'),  # Option par défaut
        ('US', 'États-Unis'),
        ('GA', 'Gabon'),
        ('GN', 'Guinée'),
        ('CA', 'Canada'),
        ('BF', 'Burkina Faso'),
        ('MA', 'Maroc'),
        ('TN', 'Tunisie'),
        ('ES', 'Espagne'),
        ('CN', 'Chine'),
        ('JP', 'Japon'),
        ('RU', 'Russie'),
        ('ML', 'Mali'),
        ('FR', 'France'),
        ('NI', 'Niger'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('', 'Sélectionnez une méthode'),  # Option par défaut
        ('card', 'Carte de crédit/débit'),
        ('bank', 'Compte bancaire'),
        ('cash', 'Espèces'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD (Dollar américain)'),
        ('XAF', 'XAF (Franc CFA BEAC)'),
        ('GNF', 'GNF (Franc guinéen)'),
        ('CAD', 'CAD (Dollar canadien)'),
        ('XOF', 'XOF (Franc CFA BCEAO)'),
        ('EUR', 'EUR (Euro)'),
        ('MAD', 'MAD (Dirham marocain)'),
        ('TND', 'TND (Dinar tunisien)'),
        ('EUR', 'EUR (Euro)'),
        ('CNY', 'CNY (Yuan chinois)'),
        ('JPY', 'JPY (Yen japonais)'),
        ('RUB', 'RUB (Rouble russe)'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers')
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    from_currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES, default='USD')
    to_currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES, default='XAF')
    from_country = models.CharField(max_length=15, choices=COUNTRY_CHOICES, default='')
    to_country = models.CharField(max_length=15, choices=COUNTRY_CHOICES, default='')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='')
    fees = models.DecimalField(max_digits=20, decimal_places=15)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=4, default=1)
    received_amount = models.DecimalField(max_digits=20, decimal_places=2)
    tracking_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfert {self.tracking_number} - {self.sender.username}"

class Agent(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    hours = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

class Currency(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    countries = models.CharField(max_length=255)
    flag = models.CharField(max_length=15)

    def __str__(self):
        return self.code

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user.username}"

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.username} a parrainé {self.referred_user.username}"

# Ajout du champ referral_code à l'utilisateur
User.add_to_class('referral_code', models.CharField(max_length=20, unique=True, blank=True, null=True))