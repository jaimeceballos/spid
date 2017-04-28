from django.forms import ModelForm
from django import forms


class LoginForm(forms.Form):
    usuario             = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control input-lg','placeholder':'Usuario'})))
    password            = forms.CharField(required=True,widget=forms.PasswordInput(attrs=dict({'class':'form-control input-lg','placeholder':'Password'})))
    dependencia         = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control input-lg','placeholder':'Dependencia'})))
    dependencia_id      = forms.CharField(required=True,widget=forms.HiddenInput())
    unidad_regional_id  = forms.CharField(required=True,widget=forms.HiddenInput())

    def clean_usuario(self):
        if not self.cleaned_data['usuario'].isdigit():
            raise forms.ValidationError("Formato de usuario incorrecto.")
        return self.cleaned_data['usuario']
