from django import forms
from django.core.exceptions import ValidationError

from .models import Bidhaa, Oda


class KikapuForm(forms.Form):
    idadi = forms.IntegerField(min_value=1, max_value=999,
                               label="Idadi")


class LipaForm(forms.Form):
    njia = forms.ChoiceField(
        choices=Oda.NJIA, label="Njia ya malipo",
        widget=forms.RadioSelect)
    simu = forms.CharField(
        required=False, max_length=15,
        label="Namba ya simu (M-Pesa: 07.. / 06..)")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("njia") == "mpesa":
            simu = cleaned.get("simu") or ""
            if not simu:
                raise ValidationError(
                    "M-Pesa inahitaji namba ya simu")
            if not simu.startswith(("07", "06")):
                raise ValidationError(
                    "Namba ya simu isiwe na 07.. au 06..")
        return cleaned


class BidhaaForm(forms.ModelForm):
    class Meta:
        model = Bidhaa
        fields = ["jina", "maelezo", "bei", "stoo", "lebo"]
