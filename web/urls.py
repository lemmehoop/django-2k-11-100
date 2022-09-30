"""notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from web.views import notes_view, main_view, note_view, note_edit_view, registration_view

urlpatterns = [
    path("", main_view, name='main'),
    path("registration/", registration_view, name='registration'),
    path("notes/", notes_view, name="notes_list"),
    path("notes/add/", note_edit_view, name="notes_add"),
    path("notes/<int:id>/", note_view, name="note"),
    path("notes/<int:id>/edit/", note_edit_view, name="note_edit"),
]
