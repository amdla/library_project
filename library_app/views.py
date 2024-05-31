from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
import requests
from .models import Book, Loan, Author, Publisher
from .forms import CustomUserCreationForm, CustomUserChangeForm, BookForm, LoanForm, AuthorForm, PublisherForm

def home(request):
    return render(request, 'library_app/home.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'lists/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = f"{user_form.cleaned_data['first_name']}.{user_form.cleaned_data['last_name']}".lower()
            user.save()
            return redirect('user-list')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'forms/user_form.html', {'user_form': user_form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user-list')
    else:
        user_form = CustomUserChangeForm(instance=user)
    return render(request, 'forms/user_form.html', {'user_form': user_form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')
    return render(request, 'forms/user_confirm_delete.html', {'user': user})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'lists/book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book_data = get_book_data_from_isbn(book.isbn)
            book.title = book_data.get('title')
            book.author = book_data.get('authors')
            book.publisher = book_data.get('publisher')
            book.publication_year = book_data.get('publishedDate')
            book.save()
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'forms/book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm(instance=book)
    return render(request, 'forms/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    return render(request, 'forms/book_confirm_delete.html', {'book': book})

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'lists/loan_list.html', {'loans': loans})

def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.loan_date = timezone.now()
            loan.book.status = 'borrowed'
            loan.book.save()
            loan.save()
            return redirect('loan-list')
    else:
        form = LoanForm()
    return render(request, 'forms/loan_form.html', {'form': form})

def loan_update(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('loan-list')
    else:
        form = LoanForm(instance=loan)
    return render(request, 'forms/loan_form.html', {'form': form})

def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.book.status = 'available'
        loan.book.save()
        loan.delete()
        return redirect('loan-list')
    return render(request, 'forms/loan_confirm_delete.html', {'loan': loan})

def get_book_data_from_isbn(isbn):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            book_data = data['items'][0]['volumeInfo']
            return {
                'title': book_data.get('title', 'N/A'),
                'authors': ', '.join(book_data.get('authors', [])),
                'publisher': book_data.get('publisher', 'N/A'),
                'publishedDate': book_data.get('publishedDate', 'N/A')
            }
    return {}

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'lists/author_list.html', {'authors': authors})

def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author-list')
    else:
        form = AuthorForm()
    return render(request, 'forms/author_form.html', {'form': form})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author-list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'forms/author_form.html', {'form': form})

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author-list')
    return render(request, 'forms/author_confirm_delete.html', {'author': author})

def publisher_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'lists/publisher_list.html', {'publishers': publishers})

def publisher_create(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('publisher-list')
    else:
        form = PublisherForm()
    return render(request, 'forms/publisher_form.html', {'form': form})

def publisher_update(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('publisher-list')
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'forms/publisher_form.html', {'form': form})

def publisher_delete(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        publisher.delete()
        return redirect('publisher-list')
    return render(request, 'forms/publisher_confirm_delete.html', {'publisher': publisher})
