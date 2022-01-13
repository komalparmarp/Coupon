from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
import datetime


# Create your views here.

def index(request):
    return HttpResponse("hello")


def get_code(request):
    """
    Return all code with all details.
    """

    codes = Coupon.objects.all()

    return render(
        request=request, template_name="codes.html", context={"codes": codes}
    )


# def get_all_order(request):
#     """
#     Return all code with all details.
#     """
#
#     codes = Order.objects.all()
#
#     return render(
#         request=request,
#         template_name="orders.html",
#         context={"codes": codes},
#     )


def add_code(request):
    """
    Add new Code form.
    """
    context = {}
    context["form"] = CouponApplyForm()

    if request.method == "POST":

        form = CouponApplyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("get_code"))
        else:
            context["form"] = form
            return render(request, "new_code.html", context)

    return render(request, "new_code.html", context)


def add_order(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon')
        order_amount = int(request.POST.get('order_amount'))

        c = Coupon.objects.get(code=request.POST.get('coupon'))  # 'c' is object of Coupon model

        user = Userprofile.objects.filter(date_of_birth=request.user.date_of_birth).first()

        if c.discounttype == "FLAT":
            total_amount = order_amount - c.discount
        else:
            birthdate = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
            today_date = datetime.date.today()
            valid_date = datetime.datetime.strftime(today_date, "%d-%m")

            if birthdate == valid_date:
                discount = order_amount * (c.discount / 100)
                total = order_amount - discount
                total_amount = total - (total * 0.1)
            else:
                discount = order_amount * (c.discount / 100)
                total_amount = order_amount - discount

        try:
            max_limit = c.max_limit
            user_limit = c.per_user_limit

            if user.is_authenticated:
                user_count = user.user_related.count()
                coupon_count = c.coupon_related.count()

                if coupon_count < max_limit:
                    if user_count >= user_limit:
                        return HttpResponse("Per user limit is over")
                    new_order = Order.objects.create(coupon=c, order_amount=order_amount,
                                                     total_amount=total_amount, user=request.user)
                    new_order.save()
                else:
                    return HttpResponse("Coupon limit is over")
        except:
            new_order = Order.objects.create(coupon=c, order_amount=order_amount,
                                             total_amount=total_amount, user=request.user)
            new_order.used += 1
            new_order.save()
        return HttpResponseRedirect('add_coupon_order')
    else:
        return render(request, "user_data.html")

        # """
    # Add User Details View.
    # """
    # context = {}
    #
    # if request.POST:
    #     data = request.POST
    #     order_amount = data.get("order_amount")
    #     coupon = data.get("coupon")
    #     # c = Coupon.objects.get(code=data.get('coupon'))  # 'c' is object of Coupon model
    #     #
    #     # user = Userprofile.objects.filter(date_of_birth=request.user.date_of_birth).first()
    #
    #     try:
    #         # if User.objects.filter(id=user_id).exists():
    #         #     user = User.objects.get(id=user_id)
    #         #     profile, created = Userprofile.objects.get_or_create(user=user)
    #         #     profile.date_of_birth = datetime.datetime.strptime(birthdate, "%m/%d/%Y")
    #         #     profile.gender = gender
    #         #     profile.save()
    #         if not int(order_amount) in range(100, 1500000):
    #             context["msg"] = "Order amount must be  between 100 to 1500001"
    #
    #         # redemption_msg = add_coupon_redemption(
    #         # request.user, order_code, int(order_amount)
    #         # )
    #         # import pdb; pdb.set_trace()
    #
    #         if not Coupon.objects.filter(code=coupon).exists():
    #             redemption_msg = "Coupon code does not exist."
    #
    #         coupon = Coupon.objects.get(code=coupon)
    #
    #         if (
    #                 timezone.now() > coupon.start_date
    #                 and timezone.now() < coupon.expiration_date
    #         ):
    #             if coupon.number_of_uses > 0:
    #                 if len(coupon.objects.filter(coupon=coupon)) < coupon.per_user_limit:
    #                     if coupon.discount_type == "percentage":
    #                         discount_amout = (order_amount * coupon.discount) / 100
    #                         amount = order_amount - discount_amout
    #                         # Check Birthdate
    #                         if timezone.now().date().strftime("%m/%d") == request.user.date_of_birth.strftime(
    #                                 "%m/%d"):
    #                             amount = amount - (amount * 10) / 100
    #
    #                         # if coupon.max_discount_amout < amount:
    #                         #     amount = order_amount - coupon.max_discount_amout
    #                     else:
    #                         amount = order_amount - coupon.discount
    #                     coupon.number_of_uses = coupon.number_of_uses - 1
    #                     coupon.save()
    #
    #                     redemption_msg = "{username} is successfully applied this {coupon_code} coupon.".format(
    #                         username=request.user.username,
    #                         coupon_code=coupon.code
    #                     )
    #                 else:
    #                     return render(request, "user_data.html", context)
    #             else:
    #                 redemption_msg = "Coupon code max limit used."
    #         else:
    #             redemption_msg = "Coupon code expiried or not activate yet."
    #
    #         context["msg"] = redemption_msg
    #         return render(request, "user_data.html", context)
    #         # else:
    #         #     context["msg"] = "User ID does not exist."
    #         #     return render(request, "user_data.html", context)
    #     except Exception as e:
    #         context["msg"] = e.__str__()
    #         return render(request, "user_data.html", context)
    #
    # return render(request, "user_data.html", context)
    #


def add_coupon_order(request):
    # coupon, order_amount):
    """
    add coupon info into order model
    """
    codes = Order.objects.all()

    return render(request, 'orders.html', {'codes': codes})
