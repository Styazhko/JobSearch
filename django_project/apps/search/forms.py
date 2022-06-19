from django import forms
from django.core.exceptions import ValidationError

from .models import Response


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter',
        )
