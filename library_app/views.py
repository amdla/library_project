from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Book, Loan
from .forms import BookForm, LoanForm, UserForm, LoanUpdateForm


def home(request):
    return render(request, 'library_app/home.html')


def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = (f"{user_form.cleaned_data['first_name']}"
                             f"|{user_form.cleaned_data['last_name']}"
                             f"|{user_form.cleaned_data['email']}")
            user.save()
            return redirect('user-list')
    else:
        user_form = UserForm()
    return render(request, 'forms/user_form.html', {'user_form': user_form})


def user_list(request):
    users = User.objects.all()
    return render(request, 'lists/user_list.html', {'users': users})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user-list')
    else:
        user_form = UserForm(instance=user)
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
            book.fill_book_data()
            book.status = 'available'
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
            loan.book.status = 'wypożyczona'
            loan.book.save()
            loan.save()
            return redirect('loan-list')
    else:
        form = LoanForm()
    return render(request, 'forms/loan_form.html', {'form': form})


def loan_update(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanUpdateForm(request.POST, instance=loan)
        if form.is_valid():
            loan = form.save(commit=False)
            if loan.is_returned:
                loan.book.status = 'available'
            else:
                loan.book.status = 'borrowed'
            loan.book.save()
            loan.save()
            return redirect('loan-list')
    else:
        form = LoanUpdateForm(instance=loan)
    return render(request, 'forms/loan_form.html', {'form': form})



def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.book.status = 'available'
        loan.book.save()
        loan.delete()
        return redirect('loan-list')
    return render(request, 'forms/loan_confirm_delete.html', {'loan': loan})


def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.is_returned = 'is_returned' in request.POST
        if loan.is_returned:
            loan.book.status = 'available'
        else:
            loan.book.status = 'borrowed'
        loan.book.save()
        loan.save()
        return HttpResponseRedirect(reverse('loan-list'))

