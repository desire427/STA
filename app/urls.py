from django.urls import path
from .views import SignUpView, UserLoginView, DashboardView
from django.contrib.auth.views import LogoutView
from .views import JournalView, JournalCreateView, JournalDetailView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("journal/", JournalView.as_view(), name="journal"),
    path("journal/nouveau/", JournalCreateView.as_view(), name="journal_create"),
    path("journal/<int:pk>/", JournalDetailView.as_view(), name="journal_detail"),
]