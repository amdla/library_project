from time import timezone
from urllib import request
from django.db import models
from django.contrib.auth.models import User
import requests

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    )
    
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, default='Autor nieznany')
    publisher = models.CharField(max_length=255, default = 'Wydawca nieznany')
    publication_date = models.CharField(max_length=10, default = 'Data wydania nieznana')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    unique_id = models.AutoField(primary_key=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.title or not self.authors or not self.publisher:
            self.fill_book_data()
        super(Book, self).save(*args, **kwargs)

def fill_book_data(self):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn}'
    response = requests.get(url)  # Use requests.get instead of urllib
    if response.status_code == 200:
        book_data = response.json()
        if "items" in book_data:
            book_info = book_data["items"][0]["volumeInfo"]
            self.title = book_info.get("title", "No Title")
            self.authors = ", ".join(book_info.get("authors", []))
            self.publisher = book_info.get("publisher", "Unknown Publisher")
            self.publication_date = book_info.get("publishedDate", "Unknown Date")
                
class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.book.title} loaned by {self.borrower.username}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # No additional fields needed for this example

    def __str__(self):
        return self.user.username
