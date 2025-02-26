from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models import Q

User = get_user_model()

class Metodologia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
        ]
        verbose_name = 'metodologia'
        verbose_name_plural = 'metodologias'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
            # Verifica se o slug já existe e adiciona um sufixo se necessário
            while Metodologia.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.nome)}-{Metodologia.objects.filter(slug__startswith=slugify(self.nome)).count() + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Ferramenta(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ferramentas/', blank=True, null=True)
    metodologia = models.ForeignKey(Metodologia, on_delete=models.CASCADE, related_name='ferramentas')
    slug = models.SlugField(max_length=200, unique=True)
    participantes = models.ManyToManyField(User, related_name='ferramentas_participantes', blank=True)
    
    class Meta:
        ordering = ['nome']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['nome']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
            # Verifica se o slug já existe e adiciona um sufixo se necessário
            while Ferramenta.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.nome)}-{Ferramenta.objects.filter(slug__startswith=slugify(self.nome)).count() + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class InstanciaFerramenta(models.Model):
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE, related_name='instancias')
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instancias_criadas')
    participantes = models.ManyToManyField(User, related_name='instancias_participantes', blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    dados = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.ferramenta.nome} (Instância de {self.dono.username})"


class PDCA(models.Model):
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE, related_name='pdcas')
    instancia = models.OneToOneField(InstanciaFerramenta, on_delete=models.CASCADE, related_name='pdca', blank=True, null=True)
    plano = models.TextField(verbose_name="Plano (Plan)")
    execucao = models.TextField(verbose_name="Execução (Do)", blank=True, null=True)
    verificacao = models.TextField(verbose_name="Verificação (Check)", blank=True, null=True)
    acao = models.TextField(verbose_name="Ação (Act)", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdcas_criados', default=100)

    def __str__(self):
        return f"PDCA para {self.ferramenta.nome}"