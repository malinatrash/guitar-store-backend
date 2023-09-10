# Generated by Django 4.2.5 on 2023-09-10 18:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0005_alter_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('ожидает', 'Ожидает'), ('в обработке', 'В обработке'), ('отправлен', 'Отправлен'), ('доставлен', 'Доставлен'), ('отменен', 'Отменен')], default='Ожидает', max_length=50),
        ),
    ]
