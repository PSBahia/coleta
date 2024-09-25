from django import forms
from .models import DadosColetados

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


    #email = forms.EmailField(required=True)

    #class Meta:
       # model = User
       # fields = ('username', 'email', 'password1', #'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    #username = forms.CharField(label='Nome de usuário')
    #password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class DadosColetadosForm(forms.ModelForm):
    class Meta:
        model = DadosColetados
        fields = (
            'numero_quarteirao',
            'numero_imovel',
            'qtd_moradores',
            'endereco',
            'tipo_imovel',
            'visita_normal',
            'pendente',
            'imovel_recuperado',
            'qtd_deposito_a1',
            'qtd_deposito_a2',
            'qtd_deposito_b',
            'qtd_deposito_c',
            'qtd_deposito_d1',
            'qtd_deposito_d2',
            'qtd_deposito_e',
            'imovel_inspecionado',
            'qtd_amostras',
            'numero_amostra_inicial',
            'numero_amostra_final',
            'imovel_tratado',
            'quantidade_larvicida',
            'quantidade_depositos_tratatados',
        )

    def clean(self):
        cleaned_data = super().clean()
        visita_normal = cleaned_data.get("visita_normal")
        pendente = cleaned_data.get("pendente")
        imovel_recuperado = cleaned_data.get("imovel_recuperado")

        if not visita_normal and not pendente and not imovel_recuperado:
            raise forms.ValidationError("Você deve marcar pelo menos uma das opções: 'Normal', 'Fechada', ou 'Recuperada'.")

            return cleaned_data
        
        if visita_normal and (pendente or imovel_recuperado):
            raise forms.ValidationError("Você deve marcar apenas uma das opções: 'Normal', 'Fechada', ou 'Recuperada'.")
            return cleaned_data
        elif pendente and (visita_normal or imovel_recuperado):
            raise forms.ValidationError("Você deve marcar apenas uma das opções: 'Normal', 'Fechada', ou 'Recuperada'.")
            return cleaned_data
        elif imovel_recuperado and (pendente or visita_normal):
            raise forms.ValidationError("Você deve marcar apenas uma das opções: 'Normal', 'Fechada', ou 'Recuperada'.")
            return cleaned_data



class FiltroDataForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
    required=False, label="Data Início")
    data_fim = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False, label="Data Fim")
    numero_quarteirao = forms.CharField(required=False)
    pendentes = forms.BooleanField(required=False, label="Imóveis Pendentes") 

