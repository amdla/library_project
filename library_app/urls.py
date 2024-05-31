from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('books/', views.book_list, name='book-list'),
    path('books/create/', views.book_create, name='book-create'),
    path('books/update/<int:pk>/', views.book_update, name='book-update'),
    path('books/delete/<int:pk>/', views.book_delete, name='book-delete'),

    path('authors/', views.author_list, name='author-list'),
    path('authors/create/', views.author_create, name='author-create'),
    path('authors/update/<int:pk>/', views.author_update, name='author-update'),
    path('authors/delete/<int:pk>/', views.author_delete, name='author-delete'),

    path('publishers/', views.publisher_list, name='publisher-list'),
    path('publishers/create/', views.publisher_create, name='publisher-create'),
    path('publishers/update/<int:pk>/', views.publisher_update, name='publisher-update'),
    path('publishers/delete/<int:pk>/', views.publisher_delete, name='publisher-delete'),

    path('loans/', views.loan_list, name='loan-list'),
    path('loans/create/', views.loan_create, name='loan-create'),
    path('loans/update/<int:pk>/', views.loan_update, name='loan-update'),
    path('loans/delete/<int:pk>/', views.loan_delete, name='loan-delete'),

    path('users/', views.user_list, name='user-list'),
    path('users/create/', views.user_create, name='user-create'),
    path('users/update/<int:pk>/', views.user_update, name='user-update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user-delete'),
]
