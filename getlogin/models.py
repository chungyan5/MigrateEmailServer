from django.db import models

# Create your models here.
class LoginPair(models.Model):
        email = models.CharField(max_length=200)
        pw = models.CharField(max_length=200)
        newPw = models.CharField(max_length=200)

	def __unicode__(self):
		return self.email
