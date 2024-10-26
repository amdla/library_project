import uuid

import requests
from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    STATUS_CHOICES = (
        ('available', 'dostępna'),
        ('borrowed', 'wypożyczona'),
    )

    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255, blank=True, default='Brak tytułu')
    authors = models.CharField(max_length=255, blank=True, default='Autor nieznany')
    publication_date = models.CharField(max_length=10, blank=True, default='Data nieznana')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    unique_id = models.AutoField(primary_key=True, unique=True)
    libraryID = models.CharField(max_length=36, unique=True, blank=True, default='')
    book_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.libraryID:
            self.libraryID = str(uuid.uuid4())
        if not self.title or not self.authors:
            self.fill_book_data()
        if not self.status:
            self.status = 'available'
        super(Book, self).save(*args, **kwargs)

    def fill_book_data(self):
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn}'
        response = requests.get(url)
        if response.status_code == 200:
            book_data = response.json()
            if "items" in book_data:
                book_info = book_data["items"][0]["volumeInfo"]
                self.title = book_info.get("title", "No Title")
                self.authors = ", ".join(book_info.get("authors", []))
                self.publication_date = book_info.get("publishedDate", "Unknown Date")

    def __str__(self):
        return str(self.unique_id)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)  # Primary key for user table
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Custom Users model
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.book.title} loaned by {self.user.username}'


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=100)
    expiration_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} subscription'


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'Notification for {self.user.username}'
