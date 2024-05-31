from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import requests

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(max_length=10, choices=(
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ))
    unique_id = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Fetch book data using Google Books API
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "items" in data:
                    item = data["items"][0]["volumeInfo"]
                    self.title = item.get("title", "")
                    self.authors = ", ".join(item.get("authors", []))
                    self.publisher = item.get("publisher", "")
                    self.publication_date = item.get("publishedDate", "1970-01-01")
            else:
                raise Exception("Unable to fetch book data")
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.isbn})"

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateField()

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.username}"
