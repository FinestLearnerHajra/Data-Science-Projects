from django.contrib import admin

# Register your models here.
from books.models import BooksInfo
from books.models import BooksCategory

admin.site.register(BooksInfo)
admin.site.register(BooksCategory)
