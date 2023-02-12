from django.db import models

# Create your models here.

class FineTunedModels(models.Model):
    model_id = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)