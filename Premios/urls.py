from django.urls import path
from Premios.views import PremiosView, CanjearPremioView

urlpatterns = [
    path('premios/', PremiosView.as_view()),
    path('premios/<int:premio_id>/canjear/', CanjearPremioView.as_view()),
]
