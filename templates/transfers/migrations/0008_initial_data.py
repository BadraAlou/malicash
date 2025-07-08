from django.db import migrations

def add_initial_data(apps, schema_editor):
    Country = apps.get_model('transfers', 'Country')
    Currency = apps.get_model('transfers', 'Currency')
    PaymentMethod = apps.get_model('transfers', 'PaymentMethod')

    Country.objects.update_or_create(
        id=1,
        defaults={'name': 'Mali', 'code': 'MLI'}
    )
    Currency.objects.update_or_create(
        id=1,
        defaults={'code': 'XOF', 'name': 'Franc CFA'}
    )
    PaymentMethod.objects.update_or_create(
        id=1,
        defaults={'name': 'Mobile Money'}
    )

class Migration(migrations.Migration):
    dependencies = [
        ('transfers', '0007_alter_currency_symbol'),
    ]
    operations = [
        migrations.RunPython(add_initial_data),
    ]