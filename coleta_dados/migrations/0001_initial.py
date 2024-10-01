# Generated by Django 5.1 on 2024-08-17 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DadosColetados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_imovel', models.CharField(max_length=100)),
                ('quantidade_moradores', models.IntegerField()),
                ('data_cadastro', models.DateField()),
            ],
        ),
    ]
