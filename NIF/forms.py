#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

class GeneratorForm(forms.Form):
    codigo_provincia    = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 2)
    codigo_ciudad       = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 2)
    numero_inicial      = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 8)
    cantidad            = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 4)

    def clean_codigo_provincia(self):
        data = self.cleaned_data['codigo_provincia']
        if not data.isdigit():
            raise forms.ValidationError('Debe Ingresar Valores Numericos.')
        return data

    def clean_codigo_ciudad(self):
        data = self.cleaned_data['codigo_ciudad']
        if not data.isdigit():
            raise forms.ValidationError('Debe Ingresar Valores Numericos.')
        return data

    def clean_numero_inicial(self):
        data = self.cleaned_data['numero_inicial']
        if not data.isdigit():
            raise forms.ValidationError('Debe Ingresar Valores Numericos.')
        return data

    def clean_cantidad(self):
        data = self.cleaned_data['cantidad']
        if not data.isdigit():
            raise forms.ValidationError('Debe Ingresar Valores Numericos.')
        return data
