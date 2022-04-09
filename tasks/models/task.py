from django.db import models

from elenas_backend_solution_test import settings


class Task(models.Model):
    """
    User task manager
    """
    title = models.CharField(
        max_length=120, unique=True, verbose_name="Título")
    description = models.CharField(
        max_length=500, verbose_name="Descripción")
    completed = models.BooleanField(default=False, verbose_name="Completado")
    creation_date = models.DateField('Fecha de Creación',
                                     auto_now=False, auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Tarea"
        ordering = ['title']

    def __str__(self):
        return self.title
