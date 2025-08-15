# spie/models.py

from django.db import models
from django.contrib.auth.models import User
from core.models import Plataforma


class Modulo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class TipoEquipamento(models.Model):
    nome = models.CharField(max_length=150, unique=True, verbose_name="Tipo de Equipamento")
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE, related_name="tipos_equipamento")
    def __str__(self): return f"{self.nome} ({self.plataforma.nome})"

class TagEquipamento(models.Model):
    chave = models.CharField(max_length=100, unique=True, verbose_name="TAG do Equipamento")
    tipo_equipamento = models.ForeignKey(TipoEquipamento, on_delete=models.CASCADE, related_name="tags")
    def __str__(self): return self.chave

class Defeito(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    def __str__(self): return self.nome

class Causa(models.Model):
    nome = models.CharField(max_length=150)
    defeito = models.ForeignKey(Defeito, on_delete=models.CASCADE, related_name="causas")
    def __str__(self): return f"{self.nome} (Defeito: {self.defeito.nome})"

class CategoriaRTI(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Categoria RTI")
    class Meta: verbose_name_plural = "Categorias RTI"
    def __str__(self): return self.nome

class Recomendacao(models.Model):
    nome = models.CharField(max_length=255)
    class Meta: verbose_name = "Recomendação"; verbose_name_plural = "Recomendações"
    def __str__(self): return self.nome

class TipoObjeto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Acesso(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Revestimento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Dano(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Objeto(models.Model):
    tipo_objeto = models.ForeignKey(TipoObjeto, on_delete=models.PROTECT)
    acesso = models.ForeignKey(Acesso, on_delete=models.PROTECT)
    revestimento = models.ForeignKey(Revestimento, on_delete=models.PROTECT)
    dano = models.ForeignKey(Dano, on_delete=models.PROTECT)
    ex_dano = models.FloatField(default=0, verbose_name="Extensão do Dano (%)")
    complemento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Objeto ID {self.id} ({self.tipo_objeto.nome})"

class ImagemObjeto(models.Model):
    objeto = models.ForeignKey(Objeto, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to='inspecao_imagens/')

    def __str__(self):
        return f"Imagem para {self.objeto}"

class Inspecao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="inspecoes", verbose_name="Inspetor")
    nota_zr = models.CharField(max_length=8, unique=True, verbose_name="Nota ZR")
    plataforma = models.ForeignKey(Plataforma, on_delete=models.PROTECT)
    modulo = models.ForeignKey(Modulo, on_delete=models.PROTECT)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    tipo_equipamento = models.ForeignKey(TipoEquipamento, on_delete=models.PROTECT, verbose_name="Tipo de Equipamento")
    tag_equipamento = models.ForeignKey(TagEquipamento, on_delete=models.PROTECT, verbose_name="TAG do Equipamento")
    defeito = models.ForeignKey(Defeito, on_delete=models.PROTECT)
    causa = models.ForeignKey(Causa, on_delete=models.PROTECT)
    categoria_rti = models.ForeignKey(CategoriaRTI, on_delete=models.PROTECT, verbose_name="Categoria RTI")
    recomendacao = models.ForeignKey(Recomendacao, on_delete=models.PROTECT, verbose_name="Recomendação")
    objetos = models.ManyToManyField(Objeto, related_name="inspecoes")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspeção ZR {self.nota_zr} em {self.plataforma.nome}"

    class Meta:
        verbose_name = "Inspeção"
        verbose_name_plural = "Inspeções"
        ordering = ['-data_criacao']