from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def is_deleted(self):
        return self.deleted_at is not None
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'