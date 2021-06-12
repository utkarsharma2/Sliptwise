from django.urls import path
from django.conf.urls import url, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserViewSet, basename='user')
router.register('event', views.EventViewSet, basename='event')
router.register('group', views.GroupViewSet, basename='group')
router.register('transactions', views.TransactionsViewSet, basename='transactions')
router.register('settle', views.SettleViewSet, basename='settle')

urlpatterns = [
    url('', include(router.urls)),
]

