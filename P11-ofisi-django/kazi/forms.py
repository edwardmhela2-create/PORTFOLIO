from django import forms

from .models import Barua, Maombi


class MaombiForm(forms.ModelForm):
    class Meta:
        model = Maombi
        fields = ["aina", "maelezo"]
        widgets = {"maelezo": forms.Textarea(attrs={"rows": 5})}


class BaruaForm(forms.ModelForm):
    class Meta:
        model = Barua
        fields = ["aina", "kichwa", "mhusika", "tarehe", "faili"]
        widgets = {"tarehe": forms.DateInput(attrs={"type": "date"})}


class KaguaForm(forms.Form):
    maoni = forms.CharField(
        required=False, max_length=300, label="Maoni (lazima kwa kukataa)",
        widget=forms.Textarea(attrs={"rows": 3}))
