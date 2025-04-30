# auth_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, department=None, contact=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(department=department, contact=contact)
            # Auto-generated password is contact+department
            if user.check_password(f"{contact}{department}"):
                return user
        except UserModel.DoesNotExist:
            return None