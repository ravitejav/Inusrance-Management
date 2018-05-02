from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    #urls to manage agent
    url(r'^$', views.home, name="home"),
    url(r'^auth/staff$', views.loginstaff, name="loginstaff"),
    url(r'^auth/user$', views.loginuser, name="loginuser"),
    url(r'^staff/logout$', views.stafflogout, name="stafflogout"),
    url(r'^staff/pass$', views.changepass, name="changepass"),
    url(r'^staff/add$', views.addcus, name="addcus"),
    url(r'^staff/change$', views.changepassword, name="changepassword"),
    url(r'^staff/addcus$', views.addtodb, name="addtodb"),
    url(r'^staff/update$', views.update, name="update"),
    url(r'^staff/updatedone$', views.updatedone, name="updatedone"),
    url(r'^staff/updatedonetodb$', views.updatedonetodb, name="updatedonetodb"),
    url(r'^staff/trans$', views.transaction, name="transaction"),
    url(r'^staff/transdone$', views.viewtrans, name="viewtrans"),
]
