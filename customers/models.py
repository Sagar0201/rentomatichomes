from django.db import models

# Create your models here.

# contact us


class ContactInfo(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.CharField(max_length=50)
    message_subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
