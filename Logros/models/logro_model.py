from django.db import models
from django.conf import settings


class Logro(models.Model):
    titulo      = models.CharField(max_length=100, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    exp         = models.PositiveIntegerField(default=0, verbose_name="EXP que otorga")
    icono       = models.CharField(max_length=10, default="🏆", verbose_name="Icono emoji")

    class Meta:
        db_table = 'logros'
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'

    def __str__(self):
        return f"{self.titulo} (+{self.exp} EXP)"


class LogroUsuario(models.Model):
    # Relación entre un usuario y un logro que ha completado
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='logros_completados'
    )
    logro = models.ForeignKey(
        Logro,
        on_delete=models.CASCADE,
        related_name='usuarios_que_lo_tienen'
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de desbloqueo")

    class Meta:
        db_table = 'logros_usuario'
        verbose_name = 'Logro de usuario'
        verbose_name_plural = 'Logros de usuarios'
        # Un usuario no puede tener el mismo logro dos veces
        unique_together = ('usuario', 'logro')

    def __str__(self):
        return f"{self.usuario.nombre} - {self.logro.titulo}"
