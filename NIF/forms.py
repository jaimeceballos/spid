#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

class GeneratorForm(forms.Form):
    codigo_provincia    = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 2)
    codigo_ciudad       = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 2)
    numero_inicial      = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'required form-control','required':'required'})),required = True, max_length = 8)
