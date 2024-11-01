
from django.contrib import admin
from django.urls import path
from .views import indexView,infoView,scan_status_view,resultView,ip_location_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',infoView, name="home"),
    path('pedido',infoView,name="pedido"),
    path('map/<str:ip>/', ip_location_view, name='ip_map'),
    path('result/', resultView, name='result'),]
