from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
                    widget=forms.PasswordInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Enter password'
                    })
                    )
                
    confirm_password = forms.CharField(
                    widget=forms.PasswordInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Confirm password'
                    })
                    )
    def clean(self):
               
               cleaned_data =super(RegistrationForm,self).clean()
               password= cleaned_data.get('password')
               confirm_password= cleaned_data.get('confirm_password')
               if password and confirm_password:
                   if password != confirm_password:
                       raise forms.ValidationError("Password does not Match")
               return cleaned_data 

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

        }

       

        
        



   