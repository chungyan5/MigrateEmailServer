from django import forms
from .models import LoginPair 

class LoginPairForm(forms.ModelForm):
	class Meta:
		model = LoginPair 
		fields = ('email', 'pw')
		widgets = {'pw': forms.PasswordInput(),}
