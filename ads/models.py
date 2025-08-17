from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='ads')

    def __str__(self):
        return self.title
