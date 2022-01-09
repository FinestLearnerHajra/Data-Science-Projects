from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from books.models import BooksCategory, BooksInfo

def index(request):
    categories = BooksCategory.objects.all()
    for cag in categories:
        cag.books_list = cag.booksinfo_set.order_by('-id')[:4]

    cart_books_list = []

    cart_books_count = 0
    for books_id, books_num in request.COOKIES.items():
        if not books_id.isdigit():
            continue
        cart_books = BooksInfo.objects.get(id=books_id)
        cart_books.books_num = books_num
        cart_books_list.append(cart_books)
        cart_books_count = cart_books_count + int(books_num)
    return render(request, 'index.html',{'categories': categories,
                                         'cart_books_list': cart_books_list,
                                         'cart_books_count': cart_books_count})

def detail(request):
    categories = BooksCategory.objects.all()

    cart_books_list = []

    cart_books_count = 0

    for books_id, books_num in request.COOKIES.items():
        if not books_id.isdigit():
            continue
        cart_books = BooksInfo.objects.get(id=books_id)

        cart_books.books_num = books_num

        cart_books_list.append(cart_books)

        cart_books_count = cart_books_count + int(books_num)

    books_id = request.GET.get('id', 1)
    books_data = BooksInfo.objects.get(id=books_id)

    return render(request, 'detail.html', {'categories': categories,
                                           'cart_books_list': cart_books_list,
                                           'cart_books_count': cart_books_count,
                                           'books_data': books_data})