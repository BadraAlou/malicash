from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Transfer

@receiver(post_save, sender=Transfer)
def envoyer_mail_si_terminé(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        try:
            send_mail(
                subject='Transfert terminé - FlyCash',
                message=(
                    f'Bonjour {instance.sender.get_full_name()},\n\n'
                    f'Votre transfert {instance.reference} a été reçu par {instance.receiver_name}.\n'
                    f'Montant : {instance.amount} {instance.from_currency.code}\n\n'
                    'Merci d\'utiliser FlyCash.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.sender.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur d'envoi d'email (signal) : {e}")