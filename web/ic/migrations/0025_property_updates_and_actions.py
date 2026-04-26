from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0024_alter_computersisod_comp_reg_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='fk_installed_in',
            field=models.ForeignKey(blank=True, db_column='fk_installed_in', help_text='Пример: стойка - основное имущество и никуда не установлена; сервер - основное имущество, установленное в стойку; HDD - резервное имущество, предназначенное для сервера.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='installed_parts', to='ic.property', verbose_name='Установлено в / Предназначено для'),
        ),
        migrations.AddField(
            model_name='property',
            name='prop_purpose',
            field=models.CharField(choices=[('Основное', 'Основное'), ('Резервное', 'Резервное')], default='Основное', max_length=20, verbose_name='Назначение'),
        ),
        migrations.AddField(
            model_name='property',
            name='prop_warranty_until',
            field=models.DateField(blank=True, null=True, verbose_name='Гарантия'),
        ),
        migrations.CreateModel(
            name='PropertyAction',
            fields=[
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_text', models.TextField(verbose_name='Действия с имуществом')),
                ('action_date', models.DateField(blank=True, null=True, verbose_name='Дата действия')),
                ('fk_property', models.ForeignKey(db_column='fk_property', on_delete=django.db.models.deletion.CASCADE, related_name='property_actions', to='ic.property', verbose_name='Имущество')),
            ],
            options={
                'verbose_name': 'Действие с имуществом',
                'verbose_name_plural': 'Действия с имуществом',
                'db_table': 'property_actions',
                'ordering': ['action_date', 'action_id'],
            },
        ),
    ]
