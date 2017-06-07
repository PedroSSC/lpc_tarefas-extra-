from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#class Usuario(models.Model):
#    nome = models.CharField('nome',max_length=200)
#    email = models.CharField('email',max_length=50)
#
#    def __str__(self):
#        return '{}'.format(self.nome)

ddddd
class Projeto(models.Model):
    nome = models.CharField('nome',max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)

class ProjetoUsuario(models.Model):
    projeto = models.ForeignKey('Projeto')
    usuario = models.OneToOneField(User)

    def __str__(self):
        return '{}'.format(self.projeto)


class Tarefa(models.Model):
    nome = models.CharField('nome',max_length=200)
    dataEHoraDeInicio = models.DateTimeField('dataEHoraDeInicio', default=timezone.now)
    projeto = models.ForeignKey('Projeto', null = True)
    usuario = models.OneToOneField(User, null = True)

    def __str__(self):
        return '{}'.format(self.nome)
