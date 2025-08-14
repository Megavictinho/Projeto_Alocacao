from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    chave = models.CharField(max_length=100, unique=True, help_text="Matrícula ou identificador único do usuário")
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Plataforma(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Alocacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='alocacoes')
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE, related_name='alocacoes')
    data_entrada = models.DateField(verbose_name="Data de Entrada")
    data_saida = models.DateField(verbose_name="Data de Saída")

    def __str__(self):
        return f"{self.usuario.nome} em {self.plataforma.nome} ({self.data_entrada} a {self.data_saida})"

    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"
        ordering = ['data_entrada']

class LogAlocacao(models.Model):
    ACAO_CHOICES = [
        ('Criação', 'Criação'),
        ('Atualização', 'Atualização'),
        ('Remoção', 'Remoção'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Usuário que realizou a ação")
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    alocacao = models.ForeignKey(Alocacao, on_delete=models.CASCADE, help_text="Alocação que foi modificada")
    detalhes = models.TextField(help_text="Detalhes da alocação no momento da ação")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.acao} por {self.usuario} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-timestamp']