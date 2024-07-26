# chat/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        if not nickname:
            raise ValueError('The Nickname field must be set')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(nickname, password, **extra_fields)

class User(AbstractUser):
    username = None
    nickname = models.CharField(max_length=50, unique=True)
    character = models.CharField(max_length=100, default='default_character.png')

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.nickname

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.nickname}: {self.message}'
