import time

from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.contrib.auth.models import User

# Create your views here.
from books.models import BooksInfo
from cart.models import OrderInfo, OrderBooks


def add_cart(request):
    books_id = request.GET.get('id', '')

    if books_id:
        prev_url = request.META['HTTP_REFERER']

        response = redirect(prev_url)

        books_count = request.COOKIES.get(books_id)

        if books_count:
            books_count = int(books_count) + 1
        else:
            books_count = 1

        response.set_cookie(books_id, books_count)

    return response


def show_cart(request):
    cart_books_list = []

    cart_books_count = 0

    cart_books_money = 0

    for books_id, books_num in request.COOKIES.items():
        if not books_id.isdigit():
            continue
        cart_books = BooksInfo.objects.get(id=books_id)

        cart_books.books_num = books_num

        cart_books.total_money = int(books_num) * cart_books.books_price

        cart_books_list.append(cart_books)

        cart_books_count = cart_books_count + int(books_num)

        cart_books_money = cart_books_money + int(books_num) * cart_books.books_price

    return render(request, 'cart.html', {'cart_books_list': cart_books_list,
                                         'cart_books_count': cart_books_count,
                                         'cart_books_money': cart_books_money})


def remove_cart(request):
    books_id = request.GET.get('id', '')
    if books_id:

        prev_url = request.META['HTTP_REFERER']

        response = redirect(prev_url)

        books_count = request.COOKIES.get(books_id, '')

        if books_count:
            response.delete_cookie(books_id)

    return response


def place_order(request):
    cart_books_list = []

    cart_books_count = 0

    cart_books_money = 0

    for books_id, books_num in request.COOKIES.items():
        if not books_id.isdigit():
            continue
        if books_id == 'csrftoken':
            continue

        cart_books = BooksInfo.objects.get(id=books_id)

        cart_books.books_num = books_num

        cart_books.total_money = cart_books.books_price * int(books_num)

        cart_books_list.append(cart_books)

        cart_books_count = cart_books_count + int(books_num)

        cart_books_money = cart_books_money + cart_books.books_price * int(books_num)

        

    return render(request, 'place_order.html', {'cart_books_list': cart_books_list,
                                                'cart_books_count': cart_books_count,
                                                'cart_books_money': cart_books_money})


def submit_order(request):
    
    addr = request.POST.get('addr', '')

    recv = request.POST.get('recv', '')

    tele = request.POST.get('tele', '')

    extra = request.POST.get('extra', '')

   

    order_info = OrderInfo()

    order_info.order_addr = addr
    order_info.order_tele = tele
    
    order_info.username = request.user
    order_info.order_extra = extra
    order_info.order_id = str(time.time() * 1000) + str(int(time.clock() * 1000000))

    order_info.save()

    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    for books_id, books_num in request.COOKIES.items():
        if not books_id.isdigit():
            continue
        if books_id == 'csrftoken':
            continue
        cart_books = BooksInfo.objects.get(id=books_id)
        order_books = OrderBooks()

        order_books.books_info = cart_books

        order_books.books_num = books_num

        order_books.books_order = order_info

        order_books.save()

        response.delete_cookie(books_id)

    return response


def submit_success(request):

    order_id = request.GET.get('id')
    u = request.user

    all=OrderInfo.objects.filter(username=u) 

   
    order_info = OrderInfo.objects.get(order_id=order_id)

    order_books_list = OrderBooks.objects.filter(books_order=order_info)
    

    total_money = 0

    total_num = 0
    for books in order_books_list:
        books.total_money = books.books_info.books_price * books.books_num

        total_money += books.total_money

        total_num += books.books_num

    return render(request, 'success.html', {'order_info': order_info,
                                            'order_books_list': order_books_list,
                                            'total_money': total_money,
                                            'total_num': total_num,
                                            'all': all})


