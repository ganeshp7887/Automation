from django.db import models

class DecryptorKeys(models.Model):
    KeyName = models.CharField(max_length=255)
    KeyValue = models.CharField(max_length=100)


    def __str__(self):
        return self.KeyValue  # String representation of the model
