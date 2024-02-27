from django.urls import path

from . import views

# app_name makes it so that in the djantgo template, the url call
# for a view would be app_name:view.name e.g item:detail in this case.
app_name = 'item'
urlpatterns = [
    path('', views.items, name='items'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new item/', views.new_item, name='new_item'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit_item, name='edit_item'),
]