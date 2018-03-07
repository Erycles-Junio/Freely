from django.contrib.auth.views import logout
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('index/', views.index_projects, name='index'),
    path('index_projects/', views.index_projects, name='index_projects'),
    path('index_services/', views.index_services, name='index_services'),
    path('register_project/', views.register_project, name='register_project'),
    path('project_details/<int:pid>/', views.project_details, name='project_details'),
    path('services/', views.services_view, name='services'),
    path('my_projects/', views.my_projects, name='myprojects'),
    path('my_services/', views.my_services, name='myservices'),
    path('delete_project/<int:pk>', views.delete_project, name='delete_project'),
    path('delete_service/<int:pk>', views.delete_service, name='delete_service'),
    path('edit_project/<int:pk>', views.edit_project, name='edit_project'),
    path('edit_service/<int:pk>', views.edit_service, name='edit_service'),
    path('send_message/<int:receiver>/<int:sender>/', views.send_message, name='send_message'),
    path('messages/', views.message_list, name='message_list'),
    path('delete_message/<int:pk>', views.delete_message, name='delete_message'),
    path('register_service/', views.register_service, name='register_service'),

]
