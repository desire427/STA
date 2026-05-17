from django.urls import path
from .views import SignUpView, UserLoginView, DashboardView, ProfileView
from django.contrib.auth.views import LogoutView
from .views import JournalView, JournalCreateView, JournalDetailView, JournalUpdateView, JournalDeleteView, CategorieView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("journal/", JournalView.as_view(), name="journal"),
    path("journal/nouveau/", JournalCreateView.as_view(), name="journal_create"),
    path("journal/<int:pk>/", JournalDetailView.as_view(), name="journal_detail"),
    path("journal/modifier/<int:pk>/", JournalUpdateView.as_view(), name="journal_update"),
    path("journal/supprimer/<int:pk>/", JournalDeleteView.as_view(), name="journal_delete"),
    path("categorie/", CategorieView.as_view(), name="categorie")
]