from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Author, Publisher, Book, BookCopy, Loan, User
from .forms import AuthorForm, PublisherForm, BookForm, BookCopyForm, LoanForm, CustomUserCreationForm, CustomUserChangeForm

def home(request):
    return render(request, 'library_app/home.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'lists/book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
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

def book_copy_list(request):
    copies = BookCopy.objects.all()
    return render(request, 'lists/book_copy_list.html', {'copies': copies})

def book_copy_create(request):
    if request.method == 'POST':
        form = BookCopyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-copy-list')
    else:
        form = BookCopyForm()
    return render(request, 'forms/book_copy_form.html', {'form': form})

def book_copy_update(request, pk):
    copy = get_object_or_404(BookCopy, pk=pk)
    if request.method == 'POST':
        form = BookCopyForm(request.POST, instance=copy)
        if form.is_valid():
            form.save()
            return redirect('book-copy-list')
    else:
        form = BookCopyForm(instance=copy)
    return render(request, 'forms/book_copy_form.html', {'form': form})

def book_copy_delete(request, pk):
    copy = get_object_or_404(BookCopy, pk=pk)
    if request.method == 'POST':
        copy.delete()
        return redirect('book-copy-list')
    return render(request, 'forms/book_copy_confirm_delete.html', {'copy': copy})

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

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'lists/loan_list.html', {'loans': loans})

def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.loan_date = timezone.now()  # Set loan_date to now
            loan.book_copy.status = 'borrowed'
            loan.book_copy.save()
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
        loan.book_copy.status = 'available'
        loan.book_copy.save()
        loan.delete()
        return redirect('loan-list')
    return render(request, 'forms/loan_confirm_delete.html', {'loan': loan})

def ajax_get_copies(request):
    book_id = request.GET.get('book')
    book_copies = BookCopy.objects.filter(book_id=book_id, is_available=True)
    html_book_copy_list = render_to_string('partials/book_copy_list_options.html', {'book_copies': book_copies})
    return JsonResponse({'html_book_copy_list': html_book_copy_list})

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
            return redirect('user-list')  # Ensure consistency here
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'forms/user_form.html', {
        'user_form': user_form,
    })

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user-list')  # Ensure consistency here
    else:
        user_form = CustomUserChangeForm(instance=user)
    return render(request, 'forms/user_form.html', {
        'user_form': user_form,
    })

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')  # Ensure consistency here
    return render(request, 'forms/user_confirm_delete.html', {'user': user})