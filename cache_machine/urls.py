"""cache_machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import BankClientAuthView, BankClientDetailView, CheckBalanceView, GetMoneyView


urlpatterns = [
    url(r'^account_active/(?P<pk>\d+)/$', BankClientDetailView.as_view(), name='account_active'),
    url(r'^card_auth/$', BankClientAuthView.as_view(), name='card_auth'),
    url(r'^check_balance/$', CheckBalanceView.as_view(), name='check_balance'),
    url(r'^get_money/$', GetMoneyView.as_view(), name='get_money'),
]
