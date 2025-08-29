from django.db import models
from django.contrib.auth.models import User

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank = True)
    is_gold_related = models.BooleanField(default = False)
    model_used = models.CharField(max_length=100, blank =True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} @ {self.created_at:%Y-%m-%d %H:%M} | gold_related={self.is_gold_related}"