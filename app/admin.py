from django.contrib import admin
from .models import Journal

# Register your models here.
@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'priorite', 'statut', 'date_creation', 'date_modification']
    list_filter = ['priorite', 'statut', 'date_creation', 'date_modification']
    search_fields = ['titre', 'contenu']
    date_hierarchy = 'date_creation'
    ordering = ['-date_creation']
    readonly_fields = ['date_creation', 'date_modification']