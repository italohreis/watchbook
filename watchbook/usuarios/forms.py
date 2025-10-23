from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import RegistroAssistido

class RegistroAssistidoForm(forms.ModelForm):
    nota = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label="Nota (de 1 a 5)"
    )
    critica = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = RegistroAssistido
        fields = ['nota', 'critica']

class FormularioLogin(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}
    ))

class FormularioCadastro(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome de usuário'}),
        }
        labels = {
            'first_name': 'Nome',
            'username': 'Nome de Usuário',
        }

    password1 = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )
    password2 = forms.CharField(
        label='Confirmação da Senha', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove os textos de ajuda
        self.fields['first_name'].help_text = None
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # Torna o nome obrigatório
        self.fields['first_name'].required = True
        self.fields['password2'].help_text = None