from django.urls import path

from targetgroups import views

app_name = 'targetgroups'
urlpatterns = [
    path('get_token/', views.get_token, name='get_token'),
    path('auth/', views.auth, name='auth'),
    path('new_group/', views.new_group, name='new_group'),
    path('group_list/', views.group_list, name='group_list'),
]