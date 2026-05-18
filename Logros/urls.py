from django.urls import path
from Logros.views import LogrosView, DesbloquearLogroView

urlpatterns = [
    path('logros/', LogrosView.as_view()),
    path('logros/<int:logro_id>/desbloquear/', DesbloquearLogroView.as_view()),
]
