# Generated by Django 4.0.3 on 2022-04-06 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_fonction', models.IntegerField()),
                ('code_groupe', models.IntegerField()),
                ('code_sous_groupe', models.IntegerField()),
                ('code_poste', models.IntegerField()),
                ('code_variete', models.IntegerField()),
                ('nom_prod', models.CharField(max_length=500)),
                ('date_creation', models.CharField(max_length=100)),
                ('imported', models.IntegerField(choices=[(1, 'Imported'), (0, 'Local')])),
                ('type_prod', models.CharField(max_length=15)),
                ('Prix_base', models.DecimalField(decimal_places=4, max_digits=12)),
                ('localy', models.IntegerField(choices=[(1, 'LOCAL'), (0, 'IMPORTED')])),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sercod', models.IntegerField()),
                ('sertyp', models.IntegerField()),
                ('prod', models.CharField(max_length=500)),
                ('Annee', models.IntegerField()),
                ('Quantité', models.IntegerField()),
                ('codpv', models.IntegerField()),
                ('nompv', models.CharField(max_length=500)),
                ('mois', models.IntegerField()),
                ('prix', models.DecimalField(decimal_places=3, max_digits=6)),
            ],
        ),
    ]
