import requests
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import DateInput
from django.utils import timezone

from .models import Book, Loan, Users, Notification, Subscription


class BookIDChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.unique_id)


class BookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')

    class Meta:
        model = Book
        fields = ('isbn',)

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        response = requests.get(url)
        if response.status_code != 200 or 'items' not in response.json():
            raise forms.ValidationError("Nieprawidłowy kod ISBN, albo nie znaleziono danych dla podanego kodu ISBN.")
        return isbn


class LoanForm(forms.ModelForm):
    book = BookIDChoiceField(queryset=Book.objects.filter(status='available'), label='ID książki')
    borrower = forms.ModelChoiceField(queryset=User.objects.all(), label='Wypożyczający')
    return_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), label='Data zwrotu')

    class Meta:
        model = Loan
        fields = ('book', 'borrower', 'return_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(status='available')
        self.fields['borrower'].queryset = User.objects.all()

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        if return_date <= timezone.now().date():
            raise forms.ValidationError("Data zwrotu musi być późniejsza niż dzisiejsza data.")
        return return_date

    def clean_book(self):
        book = self.cleaned_data.get('book')
        if book.status != 'available':
            raise forms.ValidationError("Wybrana książka nie jest dostępna.")
        return book


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Imię')
    last_name = forms.CharField(max_length=30, required=True, label='Nazwisko')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    class Meta:
        model = Users  # Referencing the new Users model
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Istnieje już użytkownik z podanym adresem email. Wprowadź inny adres.")
        return email


class LoanUpdateForm(forms.ModelForm):
    is_returned = forms.BooleanField(label='Czy zwrócona', required=False)
    return_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), label='Data zwrotu')

    class Meta:
        model = Loan
        fields = ('is_returned', 'return_date')

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        if return_date <= timezone.now().date():
            raise forms.ValidationError("Data zwrotu musi być późniejsza niż dzisiejsza data.")
        return return_date


class SubscriptionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Users.objects.all(), label='Użytkownik')
    subscription_type = forms.CharField(label='Typ Subskrypcji')
    expiration_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), label='Data Wygaśnięcia')

    class Meta:
        model = Subscription
        fields = ['user', 'subscription_type', 'expiration_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Users.objects.all()


class NotificationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Users.objects.all(), label='Użytkownik')
    message = forms.CharField(widget=forms.Textarea, label='Wiadomość')

    class Meta:
        model = Notification
        fields = ['user', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Users.objects.all()
