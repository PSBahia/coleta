from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class DadosColetados(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_quarteirao = models.CharField(max_length=100)
    numero_imovel = models.CharField(max_length=100)
    qtd_moradores = models.IntegerField(null=True, blank=True, default=0)
    endereco = models.CharField(max_length=255)
    tipo_imovel = models.CharField(
        max_length=2,
        choices=[
            ('R', 'R'),
            ('C', 'C'),
            ('TB', 'TB'),
            ('PE', 'PE'),
            ('O', 'O')
        ],
        default='R'
    )
    data_cadastro = models.DateField(auto_now_add=True)
    visita_normal = models.BooleanField(default=False)
    pendente = models.BooleanField(default=False)
    imovel_recuperado = models.BooleanField(default=False)
    qtd_deposito_a1 = models.IntegerField(null=True, blank=True, default=0)
    qtd_deposito_a2 = models.IntegerField(null=True, blank=True, default=0)
    qtd_deposito_b = models.IntegerField(null=True, blank=True, default=0)
    qtd_deposito_c = models.IntegerField(null=True, blank=True, default=0)
    qtd_deposito_d1 = models.IntegerField(null=True, blank=True, default=0)
    qtd_deposito_d2 = models.IntegerField(null=True, blank=True, default=0)  # Corrigido
    qtd_deposito_e = models.IntegerField(null=True, blank=True, default=0)
    imovel_inspecionado = models.BooleanField(default=False)
    qtd_amostras = models.IntegerField(null=True, blank=True, default=0)
    numero_amostra_inicial = models.IntegerField(null=True, blank=True, default=0)
    numero_amostra_final = models.IntegerField(null=True, blank=True, default=0)
    imovel_tratado = models.BooleanField(default=False)
    quantidade_larvicida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    quantidade_depositos_tratatados = models.IntegerField(null=True, blank=True, default=0)

    


    def __str__(self):
        return f'Imóvel {self.numero_imovel}'

