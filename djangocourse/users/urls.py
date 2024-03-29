from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.user_profile, name="user_profile"),
    path('account/', views.user_account, name="user_account"),
    path('edit-account/', views.edit_account, name="edit-account"),

    path('add-skill/', views.create_skill, name="create-skill"),
    path('edit-skill/<str:pk>/', views.update_skill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.delete_skill, name="delete-skill"),

    path('message/<str:pk>/', views.message, name="message"),
    path('inbox/', views.inbox, name="inbox"),
    path('send-message/<str:pk>/', views.send_message, name="send-message"),
]
