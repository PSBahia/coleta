from datetime import date
from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import DadosColetados
from .forms import DadosColetadosForm, FiltroDataForm

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from .models import DadosColetados
from django.db import models
from django.db.models import Sum

from django.shortcuts import render
from .models import DadosColetados

from django.utils.dateparse import parse_date

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import render
from .forms import FiltroDataForm

#codigo para app movel

# yourapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # Aqui você pode criar um token ou retornar uma resposta adequada
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


#funcoes de cadastro e login

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_usuario')
    else:
        form = CustomUserCreationForm()
    return render(request, 'coleta_dados/cadastrar_usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cadastrar_dados')  # Redirecione para uma página apropriada
    else:
        form = CustomAuthenticationForm()
    return render(request, 'coleta_dados/login_usuario.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')
#fim funcoes de cadstro e login


def gerar_relatorio_pdf(request):
    # Cria a resposta HTTP com o tipo de conteúdo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_dados.pdf"'

    # Configuração do PDF
    pdf = SimpleDocTemplate(
        response,
        pagesize=landscape(letter),
        rightMargin=0.2 * inch,
        leftMargin=0.2 * inch,
        topMargin=0.2 * inch,
        bottomMargin=0.2 * inch
    )
    elements = []

    # Estilo de texto
    styles = getSampleStyleSheet()

    # Recebendo os parâmetros de data do request
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()
    numero_quarteirao = request.GET.get('numero_quarteirao', '').strip()
    pendentes = request.GET.get('pendentes')

    hoje = date.today()

    print(f"Gerando relatório com filtros: data_inicio={data_inicio}, data_fim={data_fim}, numero_quarteirao={numero_quarteirao}")

    # Nome do usuário logado
    usuario_nome = request.user.username
    elements.append(Paragraph(f"Relatório de Dados de {usuario_nome}", styles['Title']))

     # Título e data do relatório
    date_range = f"Período: {data_inicio if data_inicio else 'Não definido'} - {data_fim if data_fim else 'Não definido'}"
    elements.append(Paragraph(date_range, styles['Normal']))

    # Filtros aplicados com base nas datas fornecidas e usuario logado
    dados = DadosColetados.objects.filter(usuario=request.user)
    if data_inicio:
        dados = dados.filter(data_cadastro__gte=parse_date(data_inicio))
    if data_fim:
        dados = dados.filter(data_cadastro__lte=parse_date(data_fim))
    if numero_quarteirao:
        dados = dados.filter(numero_quarteirao=numero_quarteirao)

    if pendentes:
        dados = dados.filter(pendente=True)

    if not data_inicio and not data_fim:
        dados = dados.filter(data_cadastro=hoje)


    # Cabeçalhos da tabela
    headers = [
        'Nº Qua', 'Nº Im', 'Hab', 'Endereço','Tipo', 'Data', 'Nor', 'Pen', 
        'Rec', 'A1', 'A2', 'B', 
        'C', 'D1', 'D2', 'E', 'Insp', 
        'Amos', 'Trat', 'Qtd.Larv', 'Dep.Trat' 
    ]
    data = [headers]

    def bool_to_sim_nao(value):
        return "X" if value else "-"

    # Adiciona os dados à tabela
    for dado in dados:
        row = [
            str(dado.numero_quarteirao),
            str(dado.numero_imovel),
            str(dado.qtd_moradores),
            str(dado.endereco),
            str(dado.tipo_imovel),
            dado.data_cadastro.strftime('%d/%m/%Y'),
            bool_to_sim_nao(dado.visita_normal),
            bool_to_sim_nao(dado.pendente),
            bool_to_sim_nao(dado.imovel_recuperado), 
            str(dado.qtd_deposito_a1),
            str(dado.qtd_deposito_a2), 
            str(dado.qtd_deposito_b),
            str(dado.qtd_deposito_c), 
            str(dado.qtd_deposito_d1),
            str(dado.qtd_deposito_d2),
            str(dado.qtd_deposito_e), 
            bool_to_sim_nao(dado.imovel_inspecionado),
            str(dado.qtd_amostras),
            bool_to_sim_nao(dado.imovel_tratado),
            str(dado.quantidade_larvicida), 
            str(dado.quantidade_depositos_tratatados),
            
        ]
        data.append(row)

    # Calcular totais
    total_moradores = dados.aggregate(Sum('qtd_moradores'))['qtd_moradores__sum'] or 0
    total_imoveis = dados.count()
    total_qtd_deposito_a1 = dados.aggregate(Sum('qtd_deposito_a1'))['qtd_deposito_a1__sum'] or 0
    total_qtd_deposito_a2 = dados.aggregate(Sum('qtd_deposito_a2'))['qtd_deposito_a2__sum'] or 0
    total_qtd_deposito_b = dados.aggregate(Sum('qtd_deposito_b'))['qtd_deposito_b__sum'] or 0
    total_qtd_deposito_c = dados.aggregate(Sum('qtd_deposito_c'))['qtd_deposito_c__sum'] or 0
    total_qtd_deposito_d1 = dados.aggregate(Sum('qtd_deposito_d1'))['qtd_deposito_d1__sum'] or 0
    total_qtd_deposito_d2 = dados.aggregate(Sum('qtd_deposito_d2'))['qtd_deposito_d2__sum'] or 0
    total_qtd_deposito_e = dados.aggregate(Sum('qtd_deposito_e'))['qtd_deposito_e__sum'] or 0
    total_qtd_amostras = dados.aggregate(Sum('qtd_amostras'))['qtd_amostras__sum'] or 0
    total_quantidade_larvicida = dados.aggregate(Sum('quantidade_larvicida'))['quantidade_larvicida__sum'] or 0
    total_quantidade_depositos_tratados = dados.aggregate(Sum('quantidade_depositos_tratatados'))['quantidade_depositos_tratatados__sum'] or 0

    # Contagem dos campos booleanos
    total_visita_normal = dados.filter(visita_normal=True).count()
    total_pendente = dados.filter(pendente=True).count()
    total_imovel_recuperado = dados.filter(imovel_recuperado=True).count()
    total_imovel_inspecionado = dados.filter(imovel_inspecionado=True).count()
    total_imovel_tratado = dados.filter(imovel_tratado=True).count()

    # Adicionar linha de totais ao rodapé da tabela
    data.append([
        'Total', '', total_moradores, '', total_imoveis, '',total_visita_normal, total_pendente, 
        total_imovel_recuperado, total_qtd_deposito_a1, total_qtd_deposito_a2, 
        total_qtd_deposito_b, total_qtd_deposito_c, total_qtd_deposito_d1, total_qtd_deposito_d2,
        total_qtd_deposito_e, total_imovel_inspecionado, total_qtd_amostras, 
        total_imovel_tratado, total_quantidade_larvicida, total_quantidade_depositos_tratados, 
        
    ])

    # Configura o estilo da tabela
    table = Table(data, colWidths=None)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        # Estilo para o rodapé
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
    ])
    table.setStyle(style)

    elements.append(table)


    # Adiciona as seções de totais
    elements.append(Paragraph("Totais:", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Criando subtabelas para os totais
    totais_data = [
        ['Total Imóveis:', str(dados.count())],
        ['Total Habitantes:', str(dados.aggregate(Sum('qtd_moradores'))['qtd_moradores__sum'])],
        ['Residenciais:', str(dados.filter(tipo_imovel='R').count())],
        ['Comerciais:', str(dados.filter(tipo_imovel='C').count())],
        ['Terrenos Baldios:', str(dados.filter(tipo_imovel='TB').count())],
        ['Pontos Estratégicos:', str(dados.filter(tipo_imovel='PE').count())],
        ['Outros:', str(dados.filter(tipo_imovel='O').count())],
    ]
    
    totais_table = Table(totais_data, colWidths=[2.5 * inch, 1.5 * inch])
    elements.append(totais_table)
    
    elements.append(Spacer(1, 12))
    
    totais_depositos = [
        ['A1:', str(dados.aggregate(Sum('qtd_deposito_a1'))['qtd_deposito_a1__sum'])],
        ['A2:', str(dados.aggregate(Sum('qtd_deposito_a2'))['qtd_deposito_a2__sum'])],
        ['B:', str(dados.aggregate(Sum('qtd_deposito_b'))['qtd_deposito_b__sum'])],
        ['C:', str(dados.aggregate(Sum('qtd_deposito_c'))['qtd_deposito_c__sum'])],
        ['D1:', str(dados.aggregate(Sum('qtd_deposito_d1'))['qtd_deposito_d1__sum'])],
        ['D2:', str(dados.aggregate(Sum('qtd_deposito_d2'))['qtd_deposito_d2__sum'])],
        ['E:', str(dados.aggregate(Sum('qtd_deposito_e'))['qtd_deposito_e__sum'])],
        ['Amostras:', str(dados.aggregate(Sum('qtd_amostras'))['qtd_amostras__sum'])],
    ]
    
    totais_depositos_table = Table(totais_depositos, colWidths=[2.5 * inch, 1.5 * inch])
    elements.append(totais_depositos_table)
    
    elements.append(Spacer(1, 12))
    
    totais_situacao = [
        ['Visitas Normais:', str(dados.filter(visita_normal=True).count())],
        ['Pendentes:', str(dados.filter(pendente=True).count())],
        ['Imóveis Recuperados:', str(dados.filter(imovel_recuperado=True).count())],
        ['Inspecionados:', str(dados.filter(imovel_inspecionado=True).count())],
        ['Tratados:', str(dados.filter(imovel_tratado=True).count())],
        ['Quantidade de Larvicida:', str(dados.aggregate(Sum('quantidade_larvicida'))['quantidade_larvicida__sum'])],
        ['Depósitos Tratados:', str(dados.aggregate(Sum('quantidade_depositos_tratatados'))['quantidade_depositos_tratatados__sum'])],
    ]
    
    totais_situacao_table = Table(totais_situacao, colWidths=[2.5 * inch, 1.5 * inch])
    elements.append(totais_situacao_table)

    # Gera o PDF
    pdf.build(elements)
    
    return response


@login_required
def cadastrar_dados(request):
    if request.method == 'POST':
        form = DadosColetadosForm(request.POST)
        if form.is_valid():
            dado = form.save(commit=False)
            dado.usuario = request.user
            dado.save()
             
            return redirect('listar_dados')
    else:
        form = DadosColetadosForm()

    return render(request, 'coleta_dados/cadastro.html', {'form': form})
    pass

@login_required
def editar_dados(request, pk):
    dados = get_object_or_404(DadosColetados, pk=pk)
    if request.method == "POST":
        form = DadosColetadosForm(request.POST, instance=dados)
        if form.is_valid():
            form.save()
            return redirect('listar_dados')  # Redireciona para a lista de dados após salvar
    else:
        form = DadosColetadosForm(instance=dados)
    return render(request, 'coleta_dados/editar_dados.html', {'form': form})

    pass

@login_required
def excluir_dados(request, pk):
    dados = get_object_or_404(DadosColetados, pk=pk)
    if request.method == "POST":
        dados.delete()
        return redirect('listar_dados')  # Redireciona para a lista de dados após excluir
    return render(request, 'coleta_dados/confirmar_exclusao.html', {'dados': dados})

    pass

class ListaDadosView(ListView):
    model = DadosColetados
    template_name = 'coleta_dados/lista.html'
    context_object_name = 'dados'


# coleta_dados/views.py
@login_required
def listar_dados(request):
    form = FiltroDataForm(request.GET or None)
    dados = DadosColetados.objects.filter(usuario=request.user)

    hoje = date.today()

    #dados = DadosColetados.objects.all()

    if form.is_valid():
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')
        numero_quarteirao = form.cleaned_data.get('numero_quarteirao')
        pendentes = form.cleaned_data.get('pendentes')

        if data_inicio:
            dados = dados.filter(data_cadastro__gte=data_inicio)
        if data_fim:
            dados = dados.filter(data_cadastro__lte=data_fim)
        if numero_quarteirao:
            dados = dados.filter(numero_quarteirao=numero_quarteirao)
        if pendentes:
            dados = dados.filter(pendente=True)
    else:
        dados = dados.filter(data_cadastro=hoje)

    total_moradores = dados.aggregate(total_moradores=models.Sum('qtd_moradores'))['total_moradores'] or 0
    total_imoveis = dados.count()
    total_R = dados.filter(tipo_imovel='R').count()
    total_C = dados.filter(tipo_imovel='C').count()
    total_TB = dados.filter(tipo_imovel='TB').count()
    total_PE = dados.filter(tipo_imovel='PE').count()
    total_O = dados.filter(tipo_imovel='O').count()
    total_deposito_a1 = sum(dado.qtd_deposito_a1 for dado in dados)
    total_deposito_a2 = sum(dado.qtd_deposito_a2 for dado in dados)
    total_deposito_b = sum(dado.qtd_deposito_b for dado in dados)
    total_deposito_c = sum(dado.qtd_deposito_c for dado in dados)
    total_deposito_d1 = sum(dado.qtd_deposito_d1 for dado in dados)
    total_deposito_d2 = sum(dado.qtd_deposito_d2 for dado in dados)
    total_deposito_e = sum(dado.qtd_deposito_e for dado in dados)
    total_amostras = sum(dado.qtd_amostras for dado in dados)
    total_larvicida = sum(dado.quantidade_larvicida for dado in dados)
    total_depositos_tratados = sum(dado.quantidade_depositos_tratatados for dado in dados)
    
    # Calculando somas dos valores True dos campos booleanos
    total_visita_normal = sum(1 for dado in dados if dado.visita_normal)
    total_pendente = sum(1 for dado in dados if dado.pendente)
    total_imovel_recuperado = sum(1 for dado in dados if dado.imovel_recuperado)
    total_imovel_inspecionado = sum(1 for dado in dados if dado.imovel_inspecionado)
    total_imovel_tratado = sum(1 for dado in dados if dado.imovel_tratado)


    context = {
        'form': form,
        'dados': dados,
        'total_moradores': total_moradores,
        'total_imoveis': total_imoveis,
        'total_R': total_R,
        'total_C': total_C,
        'total_TB': total_TB,
        'total_PE': total_PE,
        'total_O': total_O,
        'total_deposito_a1': total_deposito_a1,
        'total_deposito_a2': total_deposito_a2,
        'total_deposito_b': total_deposito_b,
        'total_deposito_c': total_deposito_c,
        'total_deposito_d1': total_deposito_d1,
        'total_deposito_d2': total_deposito_d2,
        'total_deposito_e': total_deposito_e,
        'total_amostras': total_amostras,
        'total_larvicida': total_larvicida,
        'total_depositos_tratados': total_depositos_tratados,
        'total_visita_normal': total_visita_normal,
        'total_pendente': total_pendente,
        'total_imovel_recuperado': total_imovel_recuperado,
        'total_imovel_inspecionado': total_imovel_inspecionado,
        'total_imovel_tratado': total_imovel_tratado,
    }
    return render(request, 'coleta_dados/lista.html', context)
