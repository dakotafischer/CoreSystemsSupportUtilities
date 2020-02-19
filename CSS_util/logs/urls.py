from django.urls import path
from . import views


app_name = 'logs'
urlpatterns = [
    # note: the view gets the parameter name from <str:logged_app>, logged_app is the parameter name
    path('', views.LoggedAppsView.as_view(), name='logged-apps'),
    path('logged-apps/application/<str:application>/', views.LoggedAppsView.as_view(), name='generic-list'),
    path('logged-apps/application/<str:application>/environment/<str:env>/', views.LoggedAppsView.as_view(), name='generic-list'),
    path('logged-apps/application/<str:application>/environment/<str:env>/audit-logs', views.AuditLogsView.as_view(), name='generic-list'),
    path('logged-apps/server-logs/environment/<str:env>/', views.ServerLogsView.as_view(), name='server-logs'),
    path('logged-apps/transaction-logs/environment/<str:env>/', views.TransactionLogsView.as_view(), name='transaction-logs'),
    path('logged-apps/audit-logs/environment/<str:env>/', views.AuditLogsView.as_view(), name='audit-logs'),
    path('logged-apps/request-logs/environment/<str:env>/', views.RequestLogsView.as_view(), name='request-logs'),
    path('logged-apps/admin-logs/environment/<str:env>/', views.AdminLogsView.as_view(), name='admin-logs'),
]
