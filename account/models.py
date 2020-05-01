from django.db import models
from django.conf import settings

class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    google = models.URLField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='profile/%Y/%m/%d/',blank=True, default='profile/None/avater.png')
    email_confirmed = models.BooleanField(default=False)
    active = models.BooleanField(default=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username

    # @property
    # def fullname(self):
    #     return "{} {}".format(self.first_name, self.last_name)