from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ic', '0025_property_updates_and_actions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computersisod',
            name='comp_type',
            field=models.CharField(choices=[('Стационарный', 'Стационарный'), ('Мобильный', 'Мобильный')], default='Стационарный', max_length=24, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='computersisod',
            name='comp_type_2',
            field=models.CharField(choices=[('Рабочая станция', 'Рабочая станция'), ('Ноутбук', 'Ноутбук'), ('Моноблок', 'Моноблок'), ('Планшет', 'Планшет')], default='Рабочая станция', max_length=29, verbose_name='Тип АРМ'),
        ),
        migrations.AlterField(
            model_name='propertystandarts',
            name='ps_type',
            field=models.CharField(blank=True, choices=[('Средства связи', 'Средства связи'), ('Средства вычислительной техники', 'Средства вычислительной техники'), ('Средства электронной организационной техники', 'Средства электронной организационной техники'), ('Специальная техника', 'Специальная техника')], max_length=100, verbose_name='Тип имущества'),
        ),
    ]
