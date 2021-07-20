from django import forms
from localflavor.br.forms import BRCPFField, BRCNPJField, BRZipCodeField, BRStateChoiceField
from localflavor.br.br_states import STATE_CHOICES
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from phonenumber_field.modelfields import PhoneNumberField

from .models import UserBase



class UserLoginForm(AuthenticationForm):

    email = forms.EmailField(label='Digite seu Email:', widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Email',
            'id': 'login-email'}))

    password = forms.CharField(label='Digite sua senha:', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Senha',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(max_length=254, label='Nome', help_text='Required', error_messages={'required': 'Desculpe, você precisa de um nome!'})
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Desculpe, você precisa de um email!'})
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('email',)

    
    def clean_name(self):
        user_name = self.cleaned_data['user_name']
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email já cadastrado, porfavor utilize outro!')
        return email
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não coincidem.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control', 'id': 'name', 'placeholder': 'Nome completo', 'data-sb-validations':'required'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'id': 'email', 'placeholder': 'Email', 'data-sb-validations':'required'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'id': 'password', 'placeholder': 'Senha', 'data-sb-validations':'required'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'id': 'password2', 'placeholder': 'Repita sua senha', 'data-sb-validations':'required'})


class AccountDetailsForm(forms.ModelForm):
    cpf = BRCPFField(label='CPF', help_text='Required', error_messages={'required': 'Informe seu cpf!'})
    cep = BRZipCodeField(label='CEP', help_text='CEP', error_messages={'required': 'Desculpe, você precisa informar seu CEP!'})

    class Meta:
        model = UserBase
        fields = (
            'phone_number',
            'address_line_1',
            'address_line_2',
            'city',
            'district')

    
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return cpf

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number
    
    def clean_cep(self):
        cep = self.cleaned_data['cep']
        return cep

    def clean_address_line_1(self):
        address_line_1 = self.cleaned_data['address_line_1']
        return address_line_1   
    
    def clean_address_line_2(self):
        address_line_2 = self.cleaned_data['address_line_2']
        return address_line_2

    def clean_city(self):
        city = self.cleaned_data['city']
        return city

    def clean_district(self):
        district = self.cleaned_data['district']
        return district

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update(
            {'class': 'form-control', 'id': 'cpf', 'placeholder': 'CPF', 'data-sb-validations':'required'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'id': 'phone_number', 'placeholder': 'Contato', 'data-sb-validations':'required'})
        self.fields['cep'].widget.attrs.update(
            {'class': 'form-control', 'id': 'cep', 'placeholder': 'CEP', 'data-sb-validations':'required'})
        self.fields['address_line_1'].widget.attrs.update(
            {'class': 'form-control', 'id': 'address_line_1', 'placeholder': 'Rua, Logradouro', 'data-sb-validations':'required'})
        self.fields['address_line_2'].widget.attrs.update(
            {'class': 'form-control', 'id': 'address_line_2', 'placeholder': 'Bairro', 'data-sb-validations':'required'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control', 'id': 'city', 'placeholder': 'Cidade', 'data-sb-validations':'required'})
        self.fields['district'].widget.attrs.update(
            {'class': 'form-control', 'id': 'district', 'placeholder': 'Estado', 'data-sb-validations':'required'})
