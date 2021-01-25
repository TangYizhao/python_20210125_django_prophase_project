from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.list_view),

    path("add", views.add_view),

    path("mod/<int:id>",views.mod_view),

    path("del/<int:id>",views.del_view),

    path("show/<int:id>",views.show_view),
]
