from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.add_order, name='get_user_data'),
    path('add_code', views.add_code, name='add_code'),
    # get coupon or order_amount'''

    path('get_code', views.get_code, name='get_code'),
    path('add_coupon_order', views.add_coupon_order, name='add_coupon_order')
]
