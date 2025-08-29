from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    STATUS_CHOICES = (("PENDING","PENDING"), ("SUCCESS","SUCCESS"), ("FAILED","FAILED"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_inr = models.DecimalField(max_digits=10, decimal_places=2)
    grams = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    # price snapshot used for this tx
    price_per_gram_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_authority = models.CharField(max_length=32, default="mcx")   # metals.dev 'authority'
    price_currency = models.CharField(max_length=8, default="INR")
    price_unit = models.CharField(max_length=8, default="g")
    price_timestamp = models.DateTimeField(null=True, blank=True)      # metals.dev timestamp

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="SUCCESS")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} ₹{self.amount_inr} → {self.grams}g ({self.status})"
