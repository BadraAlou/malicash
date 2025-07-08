from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Testimonial, FAQCategory, FAQ, Transfer, Agent, Currency,
    Notification, Referral
)

# Sérialiseur utilisateur simple
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Sérialiseur pour les transferts
class TransferSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = '__all__'

# Sérialiseur pour les agents
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

# Sérialiseur pour les monnaies
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

# Sérialiseur pour les notifications
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'

# Sérialiseur pour les témoignages
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

# Sérialiseur pour les catégories FAQ
class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = '__all__'

# Sérialiseur pour les FAQ
class FAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = '__all__'

# Sérialiseur pour le parrainage
class ReferralSerializer(serializers.ModelSerializer):
    referrer = UserSerializer(read_only=True)
    referred_user = UserSerializer(read_only=True)

    class Meta:
        model = Referral
        fields = '__all__'