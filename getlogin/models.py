from django.db import models

# Create your models here.
class LoginPair(models.Model):
        email = models.CharField(max_length=200,
                                 verbose_name="Amonics Email",
                                 help_text="Please input your full email address as XXX@amonics.com",
                                 )
        pw = models.CharField(max_length=200,
                              verbose_name="Password",
                              )
        newPw = models.CharField(max_length=200)

	def __unicode__(self):
		return self.email
