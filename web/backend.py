import smtplib
from django.contrib.auth.backends import BaseBackend
from .models import User

class UserIdAuthBackend(BaseBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(user_id=user_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
        
