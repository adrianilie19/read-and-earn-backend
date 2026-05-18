from django.db import models
from django.conf import settings


class EstadoChoices(models.TextChoices):
    POR_COMENZAR = "Por comenzar", "Por comenzar"
    EN_PROGRESO  = "En progreso",  "En progreso"
    COMPLETADO   = "Completado",   "Completado"


class Biblioteca(models.Model):
    # Cada entrada es un libro de un usuario concreto
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='biblioteca',
        verbose_name="Usuario"
    )

    # Datos del libro (vienen de Gutendex, solo guardamos lo esencial)
    gutendex_id  = models.PositiveIntegerField(verbose_name="ID de Gutendex")
    titulo       = models.CharField(max_length=255, verbose_name="Título")
    autor        = models.CharField(max_length=255, verbose_name="Autor", blank=True)
    portada_url  = models.URLField(blank=True, verbose_name="URL de portada")

    # Progreso de lectura
    progreso = models.PositiveIntegerField(default=0, verbose_name="Progreso (%)")
    estado   = models.CharField(
        max_length=20,
        choices=EstadoChoices.choices,
        default=EstadoChoices.POR_COMENZAR,
        verbose_name="Estado"
    )

    fecha_agregado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha en que se agregó")

    class Meta:
        db_table = 'biblioteca'
        verbose_name = 'Entrada de biblioteca'
        verbose_name_plural = 'Biblioteca'
        # Un usuario no puede tener el mismo libro dos veces
        unique_together = ('usuario', 'gutendex_id')
        ordering = ['-fecha_agregado']

    def __str__(self):
        return f"{self.titulo} - {self.usuario.nombre}"
