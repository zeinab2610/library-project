from books.forms import BooksForm, CategoryForm
from books.models import Book, Category
from django.shortcuts import redirect, render, get_object_or_404
import json
from django.contrib import messages
from django.http import HttpResponse
from books import models, forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def context_data(request):
    """Generate and return common context data for templates."""

    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host': abs_uri,
        'page_name': '',
        'page_title': '',
        'system_name': 'Library Managament System',
        'topbar': True,
        'footer': True,
    }

    return context


def login_page(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['categories'] = models.Category.objects.all().count()
    context['books'] = models.Book.objects.all().count()

    return render(request, 'home.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def category(request):
    context = context_data(request)
    context['page'] = 'category'
    context['page_title'] = "Category List"
    context['category'] = models.Category.objects.all()
    return render(request, 'category.html', context)


@login_required
def create_category(request, pk=None):
    context = context_data(request)
    context['page'] = 'manage_category'
    context['page_title'] = 'Manage Category'

    return render(request, 'create_category.html', context)


@login_required
def save_category(request):
    """Handle creation of a category."""

    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, "Category is created successfully")
            return redirect('edit-category', category_id=category.id)

        else:
            messages.error(
                request, "Category with same name exists, please try again")

    else:
        form = CategoryForm()
    return redirect('create-category')


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('edit-category', category_id=category_id)
        else:
            messages.error(request, 'Category with same name exist')

    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'edit_category.html', context)


@login_required
def update_category(request, id):
    """Handle updating of a category."""

    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        if form.is_valid():
            form.save()
            messages.success(request, 'Category is  updated successfully.')
            return redirect('/category')
    else:
        messages.error(
            request, 'Error updating category. Please check your input.')
        return redirect('/category')


@login_required
def view_category(request, pk=None):
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)

    return render(request, 'view_category.html', context)


@login_required
def delete_category(request, pk=None):
    """Handle deletion of a category."""

    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Category ID is invalid'
    else:
        try:
            models.Category.objects.filter(pk=pk).delete()
            messages.success(
                request, "Category has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Category Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def books(request):
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['books'] = models.Book.objects.all()
    return render(request, 'books.html', context)


def create_book(request):
    context = context_data(request)
    categories = Category.objects.all()
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    context['categories'] = categories

    return render(request, 'create_book.html', context)


@login_required
def save_book(request):
    """Handle creation of a book."""

    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        form = BooksForm(request.POST)
        if form.is_valid():
            book = form.save()  # Save the form data
            messages.success(request, "Book is created successfully")
            return redirect('edit-book', book_id=book.id)

        else:
            messages.error(request, "jsdjsajsdd")

    else:
        form = BooksForm()
    return redirect('create-book')


@login_required
def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)
    categories = Category.objects.all()
    print(book.category_id.id)
    if request.method == 'POST':
        form = BooksForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('edit-book', book_id=book_id)
        else:
            messages.error(request, 'Book with same name exist')
    else:
        form = BooksForm(instance=book)

    context = {
        'form': form,
        'book': book,
        'categories': categories
    }
    return render(request, 'edit_book.html', context)


@login_required
def update_book(request, id):
    """Handle editing of a book."""

    book = Book.objects.get(id=id)
    form = BooksForm(request.POST, instance=book)
    if form.is_valid():
        if form.is_valid():
            form.save()
            messages.success(request, 'Book is  updated successfully.')
            return redirect('/books')
    else:
        messages.error(
            request, 'Error updating category. Please check your input.')
        return redirect('/books')

    return redirect('/books')


@login_required
def view_book(request, pk=None):
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Book.objects.get(id=pk)

    return render(request, 'view_book.html', context)


@login_required
def delete_book(request, pk=None):
    """Handle deletion of a book."""

    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            models.Book.objects.filter(pk=pk).delete()
            messages.success(request, "Book has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Book Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")
