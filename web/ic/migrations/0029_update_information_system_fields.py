from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0028_othernetworkproperty_onp_virt_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationsystem',
            name='is_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_commissioning_order',
            field=models.TextField(blank=True, verbose_name='Основание ввода в эксплуатацию'),
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_security_level',
            field=models.CharField(blank=True, max_length=100, verbose_name='Уровень защищенности'),
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_security_level_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание уровня защищенности'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='informationsystem',
            name='is_security_class',
            field=models.CharField(blank=True, max_length=100, verbose_name='Класс защищенности'),
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_security_class_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание класса защищенности'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_threat_model_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание модели угроз безопасности'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_certificate_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание аттестата соответствия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_access_permit_system_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание разрешительной системы доступа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_technological_process_description_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание описания технологического процесса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='informationsystem',
            name='is_decommissioning_basis',
            field=models.TextField(blank=True, default='', verbose_name='Основание вывода из эксплуатации'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='informationsystemproperty',
            old_name='isp_note',
            new_name='isp_description',
        ),
        migrations.RemoveField(
            model_name='informationsystemproperty',
            name='isp_role',
        ),
        migrations.AlterField(
            model_name='informationsystemproperty',
            name='isp_description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
