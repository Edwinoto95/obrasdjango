# Generated by Django 5.1.3 on 2025-02-09 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publicas', '0003_presupuesto_monto_gastado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
            ],
        ),
    ]
