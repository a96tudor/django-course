from django.urls import path

from . import views


urlpatterns = [
    path('', views.get_routes, name='api-routes'),
    path('projects/', views.get_projects, name='api-get-projects'),
    path(
        'project/<str:pk>/', views.get_project, name='api-get-single-project'),

]
