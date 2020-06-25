from django.urls import path

from . import views

app_name = 'saml_post'
urlpatterns = [
    path('saml_profiles/', views.SamlProfilesView.as_view(), name='SamlProfilesView'),
    path('saml_post/', views.SamlPostView.as_view(), name='SamlPostView'),
    path('saml_post/<int:saml_profile_id>/', views.SamlPostView.as_view(), name='SamlPostView'),
]