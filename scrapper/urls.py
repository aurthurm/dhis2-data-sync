
from django.contrib import admin
from .views import home, update_metadata, update_data_value_sets 
from django.urls import path

app_name = "scrapper"

urlpatterns = [
    path("", home, name='home'),
    path("update-metadata", update_metadata, name='update-metadata'),
    path("update-datavaluesets", update_data_value_sets, name='update-datavaluesets')
]
