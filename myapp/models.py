from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    """
    Modèle pour gérer les catégories de documents.
    Chaque document peut être classé dans une catégorie.
    """
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Document(models.Model):
    """
    Modèle principal pour gérer les documents.
    Stocke les informations sur chaque document :
    - titre : nom du document
    - description : brève description du contenu
    - fichier : le fichier physique stocké sur le serveur
    - date_creation : date et heure d'ajout automatique
    - categorie : lien vers la catégorie (peut être null)
    - auteur : utilisateur qui a créé le document
    """
    titre = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True)
    fichier = models.FileField(upload_to='documents/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.titre
    

    





