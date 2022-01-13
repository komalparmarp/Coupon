from django import forms
from .models import *


class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
