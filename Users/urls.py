from django.urls import path
from Users.views import RegisterView, LoginView, PerfilView

urlpatterns = [
    path('registro/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('perfil/', PerfilView.as_view()),
]
