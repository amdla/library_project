from django.urls import path

from library_app import views

urlpatterns = [
    path('', views.home, name='home'),

    path('books/', views.book_list, name='book-list'),
    path('books/create/', views.book_create, name='book-create'),
    path('books/update/<int:pk>/', views.book_update, name='book-update'),
    path('books/delete/<int:pk>/', views.book_delete, name='book-delete'),

    path('loans/', views.loan_list, name='loan-list'),
    path('loans/create/', views.loan_create, name='loan-create'),
    path('loans/update/<int:pk>/', views.loan_update, name='loan-update'),
    path('loans/delete/<int:pk>/', views.loan_delete, name='loan-delete'),
    path('loan/return/<int:pk>/', views.loan_return, name='loan-return'),

    path('users/', views.user_list, name='user-list'),
    path('users/create/', views.user_create, name='user-create'),
    path('users/update/<int:pk>/', views.user_update, name='user-update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user-delete'),

    path('subscriptions/', views.subscription_list, name='subscription-list'),
    path('subscriptions/create/', views.subscription_create, name='subscription-create'),
    path('subscriptions/update/<int:pk>/', views.subscription_update, name='subscription-update'),
    path('subscriptions/delete/<int:pk>/', views.subscription_delete, name='subscription-delete'),

    path('notifications/', views.notification_list, name='notification-list'),
    path('notifications/create/', views.notification_create, name='notification-create'),
    path('notifications/update/<int:pk>/', views.notification_update, name='notification-update'),
    path('notifications/delete/<int:pk>/', views.notification_delete, name='notification-delete'),
]
