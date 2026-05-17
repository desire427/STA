from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Journal, ActionLog, Categorie

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("dashboard")
    template_name = "signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserLoginView(LoginView):
    template_name = "login.html"

class UserIsOwnerMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est l'auteur de l'objet."""
    def test_func(self):
        journal = self.get_object()
        return journal.auteur == self.request.user

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profile.html"

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # On récupère les données globales pour la traçabilité complète
        all_entries = Journal.objects.select_related('categorie').all()
        
        # Statistiques basées sur l'état actuel des notes
        stats = all_entries.aggregate(
            opened=Count('id', filter=Q(statut='ouvert')),
            in_progress=Count('id', filter=Q(statut='en_cours')),
            resolved=Count('id', filter=Q(statut='resolu'))
        )
        
        total_actions = ActionLog.objects.count()
        
        completion_rate = 0
        total_current = all_entries.count()
        if total_current > 0:
            completion_rate = (stats['resolved'] / total_current) * 100
        
        context['total_entries'] = total_actions  # Utilise le compte de l'historique
        context['open_entries'] = stats['opened']
        context['in_progress_entries'] = stats['in_progress']
        context['resolved_entries'] = stats['resolved']
        context['completion_rate'] = round(completion_rate)
        context['categories'] = Categorie.objects.all()

        # Affiche les notes récemment modifiées (y compris créations)
        context['recent_activities'] = all_entries.order_by('-date_modification')[:6]
        return context

class JournalView(LoginRequiredMixin, generic.ListView):
    model = Journal
    template_name = "liste_ent.html"
    context_object_name = "journaux"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context

class CategorieView(LoginRequiredMixin, generic.CreateView):
    model = Categorie
    fields = ['nom', 'couleur']
    template_name = "categorie.html"
    success_url = reverse_lazy("categorie")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.annotate(nb_activites=Count('journaux'))
        return context

class JournalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Journal
    fields = ['titre', 'contenu', 'image', 'priorite', 'statut', 'categorie']
    template_name = "liste_ent.html"
    success_url = reverse_lazy("journal")

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journaux'] = Journal.objects.all()
        context['categories'] = Categorie.objects.all()
        return context

class JournalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Journal
    template_name = "details.html"
    context_object_name = "journal"

class JournalUpdateView(LoginRequiredMixin, UserIsOwnerMixin, generic.UpdateView):
    model = Journal
    fields = ['titre', 'contenu', 'image', 'priorite', 'statut', 'categorie']
    template_name = "update_ent.html"
    context_object_name = "journal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('journal_detail', kwargs={'pk': self.object.pk})

class JournalDeleteView(LoginRequiredMixin, UserIsOwnerMixin, generic.DeleteView):
    model = Journal
    template_name = "journal_confirm_delete.html"
    success_url = reverse_lazy("journal")
