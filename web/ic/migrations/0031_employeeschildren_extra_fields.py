from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0030_simplify_information_systems'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeschildren',
            name='empc_home_address',
            field=models.CharField(blank=True, max_length=250, verbose_name='Адрес проживания'),
        ),
        migrations.AddField(
            model_name='employeeschildren',
            name='empc_study_place',
            field=models.CharField(blank=True, max_length=250, verbose_name='Обучается в'),
        ),
        migrations.AddField(
            model_name='employeeschildren',
            name='empc_mobile_phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='Мобильный телефон'),
        ),
    ]
