from django.db import models
from django.contrib.auth.models import User

class Journal(models.Model):
    PRIORITY_CHOICES = [
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
    ]

    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu / Terminé'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre de l'activité")
    contenu = models.TextField(verbose_name="Description détaillée")
    image = models.ImageField(upload_to='journaux/%Y/%m/%d/', blank=True, null=True, verbose_name="Image de preuve")
    priorite = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normale')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='ouvert')
    
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journaux')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Entrée de journal"
        verbose_name_plural = "Entrées de journal"

    def __str__(self):
        return f"{self.titre} - {self.auteur.username}"