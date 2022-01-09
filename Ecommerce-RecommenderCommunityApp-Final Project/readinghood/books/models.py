from django.db import models

# Create your models here.
class BooksCategory(models.Model):
    category_name = models.CharField(max_length=30)

    category_img = models.ImageField(upload_to='catogory')

class BooksInfo(models.Model):
    books_name = models.CharField(max_length=100)

    books_author = models.CharField(max_length=50)

    books_price = models.IntegerField(default=0)

    books_description = models.CharField(max_length=2000)

    books_img = models.ImageField(upload_to='books')

    books_quantity = models.IntegerField(default=0)

    books_category = models.ForeignKey('BooksCategory', on_delete=models.CASCADE)