from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User                                                                           # Se basa en el model User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']    # Los campos se pueden ver desde la tabla auth_user en la base de datos