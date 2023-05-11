from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
import decimal

from django.db import models
from django.db.models import Model, CharField, FloatField, ForeignKey

class produit(models.Model):
    code_fonction= models.IntegerField()
    code_groupe= models.IntegerField()
    code_sous_groupe= models.IntegerField()
    code_poste= models.IntegerField()
    code_variete= models.IntegerField()
    nom_prod = models.CharField(max_length =500)
    date_creation =models.CharField(max_length=100)
    
    IMPORTED_CHOICES=(
        (1,'Imported'),
        (0,'Local'),
    )
    imported =models.IntegerField(choices=IMPORTED_CHOICES)
    type_prod = models.CharField(max_length =15)
    

    
    Prix_base = models.DecimalField(decimal_places=4,max_digits=12)
   
    LOCALY_CHOICES=(
        (1,'LOCAL'),
        (0,'IMPORTED')
    )
    
    localy =models.IntegerField (choices=LOCALY_CHOICES)


    






class Serie(models.Model):
    sercod=models.IntegerField()
    sertyp=models.IntegerField()
    prod=models.CharField(max_length =500)
   
    Annee=models.IntegerField()
    Quantité = models.IntegerField()
    codpv = models.IntegerField()
    nompv=models.CharField(max_length =500)
    mois=models.IntegerField()
    prix = models.DecimalField(decimal_places=3,max_digits=6) 
        



