from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.


class profile(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    # description = models.TextField(null=True) Makes the field allow for empty description fields
    description = models.TextField(default='description default text')
    # location = models.CharField(
    #    max_length=120, default='my location default', blank=True, null=True)
    # job = models.CharField(max_length=120, null=True)

    # This will give the reference to the model, what you see when selecting between profiles
    def __str__(self):
        print("sup")
        return self.name


class userStripe(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.stripe_id:
            return str(self.stripe_id)
            print("hi")
        else:
            return self.user.username


def stripeCallback(sender, request, user, **kwargs):
    user_stripe_account, created = userStripe.objects.get_or_create(user=user)
    if created:
        print('created for %s' % (user.username))
    if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=user.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()


def profileCallback(sender, request, user, **kwargs):
    userProfile, is_created = profile.objects.get_or_create(user=user)
    if is_created:
        userProfile.name = user.username
        userProfile.save()


user_logged_in.connect(stripeCallback)
# user_logged_in.connect(profileCallback)
user_signed_up.connect(profileCallback)
user_signed_up.connect(stripeCallback)
