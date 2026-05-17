from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    couleur = models.CharField(max_length=20, default="#1a237e", verbose_name="Couleur")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom

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
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='journaux', verbose_name="Catégorie")
    
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journaux')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Entrée de journal"
        verbose_name_plural = "Entrées de journal"

    def __str__(self):
        return f"{self.titre} - {self.auteur.username}"

    def get_absolute_url(self):
        return reverse('journal_detail', kwargs={'pk': self.pk})

class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('creation', 'Création'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    ]
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    journal_titre = models.CharField(max_length=200)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

@receiver(post_save, sender=Journal)
def log_journal_save(sender, instance, created, **kwargs):
    action = 'creation' if created else 'modification'
    ActionLog.objects.create(
        action_type=action,
        journal_titre=instance.titre,
        utilisateur=instance.auteur
    )

@receiver(post_delete, sender=Journal)
def log_journal_delete(sender, instance, **kwargs):
    ActionLog.objects.create(
        action_type='suppression',
        journal_titre=instance.titre,
        utilisateur=instance.auteur
    )