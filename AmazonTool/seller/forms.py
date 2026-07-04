from django import forms
from .models import Campaign 

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ["name", "type", "budget", "target_acos"]

        labels = {
            'name': 'CAMPAIGN NAME',
            'type': 'CAMPAIGN TYPE',
            'budget': 'DAILY BUDGET ($)',
            'target_acos': 'TARGET ACOS (%)',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Yoga Mat - Broad Match',
                'class': 'form-control'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'budget': forms.NumberInput(attrs={
                'value': '50',
                'min': '1',
                'class': 'form-control'
            }),
            'target_acos': forms.NumberInput(attrs={
                'value': '25',
                'min': '0',
                'max': '100',
                'class': 'form-control'
            }),
        }
