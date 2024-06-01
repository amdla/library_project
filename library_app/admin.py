from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Book, Loan, UserProfile



# Admin for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'authors', 'publisher', 'publication_date', 'status', 'unique_id')
    list_filter = ('status', 'publisher')
    search_fields = ('title', 'isbn', 'authors', 'publisher')

# Admin for Loan
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'loan_date', 'return_date')
    list_filter = ('loan_date', 'return_date')
    search_fields = ('borrower__username', 'book__title')

# Inline for UserProfile to be edited within User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

# Extend existing User admin to include UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
