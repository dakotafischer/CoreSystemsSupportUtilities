from django.urls import path

from . import views

app_name = 'saml_post'
urlpatterns = [
    path('', views.SamlPostView.as_view(), name='SamlPostView'),
]
