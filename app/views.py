from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Journal

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

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

class JournalView(LoginRequiredMixin, generic.ListView):
    model = Journal
    template_name = "liste_ent.html"
    context_object_name = "journaux"

class JournalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Journal
    fields = ['titre', 'contenu', 'image', 'priorite', 'statut']
    template_name = "liste_ent.html"
    success_url = reverse_lazy("journal")

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journaux'] = Journal.objects.all()
        return context

class JournalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Journal
    template_name = "details.html"
    context_object_name = "journal"

class JournalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Journal
    fields = ['titre', 'contenu', 'image', 'priorite', 'statut']
    template_name = "update_ent.html"
    context_object_name = "journal"

    def get_success_url(self):
        return reverse_lazy('journal_detail', kwargs={'pk': self.object.pk})
