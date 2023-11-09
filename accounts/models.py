from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=50,null=True)
    image = models.ImageField(default='/admin.png',null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return self.user.username


