from django import forms

from .models import Akaunti, Miamala, Mkopo, Wateja


class WatejaForm(forms.ModelForm):
    class Meta:
        model = Wateja
        fields = ["jina", "simu", "barua_pepe", "anwani"]


class FedhaForm(forms.Form):
    akaunti = forms.ModelChoiceField(queryset=Akaunti.objects.all(),
                                     label="Akaunti")
    aina = forms.ChoiceField(choices=Miamala.AINATU, label="Aina")
    kiasi = forms.DecimalField(min_value=1, label="Kiasi (Tsh)",
                               max_digits=12, decimal_places=2)
    maelezo = forms.CharField(required=False, max_length=200,
                              label="Maelezo")


class MkopoForm(forms.ModelForm):
    class Meta:
        model = Mkopo
        fields = ["wateja", "kiasi", "riba_asilimia"]
