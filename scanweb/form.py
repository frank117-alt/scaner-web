from django import forms
from .validator import validate_ip_domain  # Importa el validador
class IPDomainForm(forms.Form):
    host = forms.CharField(max_length=255, validators=[validate_ip_domain],widget=forms.TextInput(attrs={'class':'search-input','placeholder': 'Ingresa IP o dominio'}))