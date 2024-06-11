import uuid
from django.db import models
from django.contrib.auth.models import User
import requests


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


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.book.title} loaned by {self.borrower.first_name} {self.borrower.last_name}'
