from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'	# all fields in Profile model
		exclude = ['user']


