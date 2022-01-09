from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class OrderInfo(models.Model):
    status = (
        (1, 'to be paid'),
        (2, 'to be delivered'),
        (3, 'to be received'),
        (4, 'Finished')
    )

    order_id = models.CharField(max_length=100)

    order_addr = models.CharField(max_length=100)

    order_recv = models.CharField(max_length=50)

    order_tele = models.CharField(max_length=10)

    order_fee = models.IntegerField(default=10)

    order_extra = models.CharField(max_length=200)

    order_status = models.IntegerField(default=1, choices=status)

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    

class OrderBooks(models.Model):
    books_info = models.ForeignKey('books.BooksInfo', on_delete=models.CASCADE)

    books_num = models.IntegerField()

    books_order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE)