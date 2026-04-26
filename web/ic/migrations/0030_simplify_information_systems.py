from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0029_update_information_system_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_commissioning_order',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_security_level_basis',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_security_class_basis',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_threat_model_basis',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_certificate_basis',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_access_permit_system_basis',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_technological_process_description_basis',
        ),
        migrations.RemoveField(
            model_name='informationsystem',
            name='is_decommissioning_basis',
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_name',
            field=models.TextField(unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_date_commissioning',
            field=models.TextField(blank=True, null=True, verbose_name='Введена в эксплуатацию'),
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_security_level',
            field=models.TextField(blank=True, verbose_name='Уровень защищенности'),
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_security_class',
            field=models.TextField(blank=True, verbose_name='Класс защищенности'),
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_date_decommissioning',
            field=models.TextField(blank=True, null=True, verbose_name='Выведена из эксплуатации'),
        ),
        migrations.AlterModelOptions(
            name='informationsystemproperty',
            options={
                'ordering': ['fk_information_system', 'fk_property'],
                'verbose_name': 'Связь имущества с информационной системой',
                'verbose_name_plural': 'Связи имущества с информационными системами',
            },
        ),
    ]
