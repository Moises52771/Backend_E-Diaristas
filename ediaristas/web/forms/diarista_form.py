import json
from django import forms
from .. import models
from ..services import cep_service


class DiaristaForm(forms.ModelForm):
    cpf = forms.CharField(widget=forms.TextInput(attrs={'data-mask': "000.000.000-00"}))
    cep = forms.CharField(widget=forms.TextInput(attrs={'data-mask': "00000-000"}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'data-mask': "(00) 0 0000-0000"}))

    class Meta:
        model = models.Diaristas
        #fields = '__all__'
        exclude = ('codigo_ibge', )


    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return cpf.replace(".", "").replace("-", "")


    def clean_cep(self):
        cep = self.cleaned_data['cep']
        cep_formatado = cep.replace("-", "")
        response = cep_service.buscar_cidade_cep(cep_formatado)
        cidade_api = json.loads(response.content)
        if response.status_code == 400:
            raise forms.ValidationError("O CEP informado está incorreto")
        elif 'erro' in cidade_api:
            raise forms.ValidationError("O CEP informado não foi encontrado")

        return cep.replace("-", "")


    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        return telefone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")


    def save(self, commit=True):
        instance = super(DiaristaForm, self).save(commit=False)
        response = cep_service.buscar_cidade_cep(self.cleaned_data['cep'])
        cidade_api = json.loads(response.content)
        instance.codigo_ibge = cidade_api['ibge']
        instance.save()
        return instance
