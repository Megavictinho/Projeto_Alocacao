from django.db import models

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