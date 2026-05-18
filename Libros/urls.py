from django.urls import path
from Libros.views import BibliotecaView, BibliotecaDetalleView

urlpatterns = [
    path('biblioteca/', BibliotecaView.as_view()),
    path('biblioteca/<int:libro_id>/', BibliotecaDetalleView.as_view()),
]
