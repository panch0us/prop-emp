from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0026_fix_choices_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationSystem',
            fields=[
                ('is_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_name', models.TextField(unique=True, verbose_name='Название')),
                ('is_date_commissioning', models.DateField(blank=True, null=True, verbose_name='Введена в эксплуатацию')),
                ('is_commissioning_order', models.TextField(blank=True, verbose_name='Введена в эксплуатацию приказом')),
                ('is_security_level', models.TextField(blank=True, verbose_name='Уровень защищенности')),
                ('is_security_class', models.TextField(blank=True, verbose_name='Класс защищенности')),
                ('is_threat_model', models.TextField(blank=True, verbose_name='Модель угроз безопасности')),
                ('is_certificate', models.TextField(blank=True, verbose_name='Аттестат соответствия по требованиям безопасности информации ИС')),
                ('is_access_permit_system', models.TextField(blank=True, verbose_name='Разрешительная система доступа')),
                ('is_technological_process_description', models.TextField(blank=True, verbose_name='Описание технологического процесса')),
                ('is_security_admin_instruction', models.TextField(blank=True, verbose_name='Инструкция администратора безопасности')),
                ('is_user_instruction', models.TextField(blank=True, verbose_name='Инструкция пользователя')),
                ('is_password_protection_instruction', models.TextField(blank=True, verbose_name='Инструкция по созданию и применению парольной защиты')),
                ('is_antivirus_instruction', models.TextField(blank=True, verbose_name='Инструкция по организации антивирусной защиты')),
                ('is_confidential_information_list', models.TextField(blank=True, verbose_name='Перечень сведений конфиденциального характера')),
                ('is_room_access_instruction', models.TextField(blank=True, verbose_name='Инструкция доступа в помещение, в которых ведется обработка персональных данных')),
                ('is_access_rights_regulation', models.TextField(blank=True, verbose_name='Положение о разграничении прав доступа к обрабатываемой информации')),
                ('is_server_room_access_persons', models.TextField(blank=True, verbose_name='Список лиц, имеющих право доступа в серверное помещение')),
                ('is_date_decommissioning', models.DateField(blank=True, null=True, verbose_name='Выведена из эксплуатации')),
            ],
            options={
                'verbose_name': 'Информационная система',
                'verbose_name_plural': 'Информационные системы',
                'db_table': 'ic_information_systems',
                'ordering': ['is_name'],
            },
        ),
        migrations.CreateModel(
            name='InformationSystemProperty',
            fields=[
                ('isp_id', models.AutoField(primary_key=True, serialize=False)),
                ('isp_role', models.TextField(blank=True, verbose_name='Роль')),
                ('isp_note', models.TextField(blank=True, verbose_name='Примечание')),
                ('fk_information_system', models.ForeignKey(db_column='fk_information_system', on_delete=django.db.models.deletion.CASCADE, related_name='system_properties', to='ic.informationsystem', verbose_name='Информационная система')),
                ('fk_property', models.ForeignKey(db_column='fk_property', on_delete=django.db.models.deletion.CASCADE, related_name='information_system_links', to='ic.property', verbose_name='Имущество')),
            ],
            options={
                'verbose_name': 'Имущество информационной системы',
                'verbose_name_plural': 'Имущество информационных систем',
                'db_table': 'ic_information_system_property',
                'ordering': ['fk_information_system', 'fk_property'],
                'unique_together': {('fk_information_system', 'fk_property')},
            },
        ),
    ]
