from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
# from testapp.core.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

DISCOUNT_CHOICES = (("percentage", "Percentage"), ("flat", "Flat"))
GENDER_CHOICES = (("m", "Male"), ("f", "Female"))


class Coupon(models.Model):

    def validate_date(value):
        v = timezone.now()
        if value < v:
            raise ValidationError("please don't enter a pastdate")

    def validate_start(start):

        d = timezone.now()
        if start > d:
            raise ValidationError("enter valid date ")

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get("start_date")
    #     expiration_date = cleaned_data.get("end_date")
    #     if expiration_date < start_date:
    #         raise ValidationError("End date should be greater than start date.")

    code = models.CharField(
        max_length=6,
        unique=True,
        # help_text="Only uppercase letters & numbers are allowed.",
        validators=[
            RegexValidator(
                "^[A-Z0-9]*$", "Only uppercase letters & numbers are allowed.",

            )
        ],
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    start_date = models.DateTimeField(validators=[validate_start], null=True, blank=True)
    expiration_date = models.DateTimeField(validators=[validate_date], null=True, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_CHOICES)
    discount = models.PositiveIntegerField()
    number_of_uses = models.PositiveIntegerField(
        # help_text="How many times this coupon will be used.", default=1
    )

    per_user_limit = models.PositiveIntegerField()

    # is_active = models.BooleanField(default=True)

    # is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def __enumerable_to_display(self, enumerables, enum_value):
        """Get the human readable value from an enumerable list of key-value pairs."""
        return dict(enumerables)[enum_value]

    @property
    def display_gender(self):
        """
        return coupon gender
        """
        return self.__enumerable_to_display(GENDER_CHOICES, self.gender)


class Userprofile(AbstractUser):
    date_of_birth = models.DateField(blank=False, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    def __str__(self):
        return "{}".format(self.username)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_related')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE,related_name='coupon_related')
    order_amount = models.PositiveIntegerField()
        # validators=[MinValueValidator(100),MaxValueValidator(150000)])
    total_amount = models.PositiveIntegerField(
        # help_text="Order total amount after code redemption applied."
    )

    def __str__(self):
        return "{} - {}".format(self.user.username, self.coupon.code)
