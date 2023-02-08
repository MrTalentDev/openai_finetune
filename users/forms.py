from django.contrib.auth.forms import UserCreationForm
from .models import User
 
class SignUpForm(UserCreationForm):
    password2 = None
    class Meta:
        model = User
        fields = ('email','name',)