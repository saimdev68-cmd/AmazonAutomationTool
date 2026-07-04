from django import forms
from seller.models import Seller
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'id': f'id_{field_name}'})


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['business_name', 'timezone']
        widgets = {
            'business_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'timezone': forms.Select(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'id': f'id_{field_name}'})