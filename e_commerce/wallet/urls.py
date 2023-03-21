
from django.urls import path
from wallet import views

urlpatterns = [
    path('fund_deposit/', views.FundDeposit, name='fund_deposit'),
    path('coupon_list/',views.CouponList, name='coupon_list'),
    path('generate_coupons/',views.GenerateCoupons, name='generate_coupons'),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon, name='delete_coupon')
]
