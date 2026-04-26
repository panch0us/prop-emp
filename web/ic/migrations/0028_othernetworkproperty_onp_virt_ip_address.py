from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0027_information_systems'),
    ]

    operations = [
        migrations.AddField(
            model_name='othernetworkproperty',
            name='onp_virt_ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='Виртуальный IP-адрес'),
        ),
    ]
