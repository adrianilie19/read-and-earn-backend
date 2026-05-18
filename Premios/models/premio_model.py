from django.db import models
from django.conf import settings


class Premio(models.Model):
    titulo     = models.CharField(max_length=200, verbose_name="Título del libro")
    autor      = models.CharField(max_length=200, verbose_name="Autor", blank=True)
    coste_exp  = models.PositiveIntegerField(verbose_name="Coste en EXP")
    stock      = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    portada_url = models.URLField(blank=True, verbose_name="URL de portada")
    is_active  = models.BooleanField(default=True, verbose_name="¿Disponible?")

    class Meta:
        db_table = 'premios'
        verbose_name = 'Premio'
        verbose_name_plural = 'Premios'
        ordering = ['coste_exp']

    def __str__(self):
        return f"{self.titulo} ({self.coste_exp} EXP)"


class Canje(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='canjes'
    )
    premio = models.ForeignKey(
        Premio,
        on_delete=models.CASCADE,
        related_name='canjes'
    )
    exp_gastada = models.PositiveIntegerField(verbose_name="EXP gastada")
    fecha       = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del canje")

    class Meta:
        db_table = 'canjes'
        verbose_name = 'Canje'
        verbose_name_plural = 'Canjes'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.usuario.nombre} canjeó {self.premio.titulo}"
