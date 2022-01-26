from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import OrderBy


from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.utils.timezone import timezone

# Create your models here.


class Rentales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oner_mobile_no = models.IntegerField(default=0)
    home_image = models.ImageField(upload_to="static/images")
    home_name = models.CharField(max_length=50, default="unknown")
    home_city = models.CharField(max_length=50, )
    home_info = models.CharField(max_length=500,)
    home_address = models.CharField(max_length=200,)
    home_rent = models.IntegerField(default=0)

    def __str__(self):
        return self.home_name


class Profile(models.Model):
    # Delete profile when user is deleted
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='static/profile_pic', null=True, default='abc.png')

    def __str__(self):
        # show how we want it to be displayed
        return f'{self.profile_user.username} Profile'

# create by sagar kakade


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profile_user=instance)
    instance.profile.save()


class Chat(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200, default="no message")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
