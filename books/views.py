from django.shortcuts import render, redirect
from books.forms import BooksForm, CategoryForm
from books.models import Book, Category
import datetime
from django.shortcuts import redirect, render, get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from books import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Create your views here.
def create_book(request):
    context = context_data(request)
    categories = Category.objects.all()
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    context['categories'] = categories
    
    return render(request, 'create_book.html', context)


def update_category(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST,instance = category)
    if form.is_valid():
      if form.is_valid():
        form.save()
        messages.success(request, 'Category is  updated successfully.')
        return redirect('/category')
    else:
        messages.error(request, 'Error updating category. Please check your input.')
        return redirect('/category')

def update_book(request, id):
    book = Book.objects.get(id=id)
    form = BooksForm(request.POST,instance = book)
    if form.is_valid():
      if form.is_valid():
        form.save()
        messages.success(request, 'Book is  updated successfully.')
        return redirect('/books')
    else:
        messages.error(request, 'Error updating category. Please check your input.')
        return redirect('/books')
   
    return redirect('/books')

def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Library Managament System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

def login_page(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['categories'] = models.Category.objects.all().count()
    context['books'] = models.Book.objects.all().count()


    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

@login_required
def users(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = User.objects.exclude(pk=request.user.pk).filter(is_superuser = False).all()
    return render(request, 'users.html', context)

@login_required
def save_user(request):
    resp = { 'status': 'failed', 'msg' : '' }
    print(request.method)
    if request.method == 'POST':
        print('HERR')
        post = request.POST
        if not post['id'] == '':
            user = User.objects.get(id = post['id'])
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_user(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = User.objects.get(id=pk)
    
    return render(request, 'manage_user.html', context)

@login_required
def delete_user(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def category(request):
    context = context_data(request)
    context['page'] = 'category'
    context['page_title'] = "Category List"
    context['category'] = models.Category.objects.all()
    return render(request, 'category.html', context)

def save_category(request):
    resp = { 'status' : 'failed', 'msg':''}

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()  # Save the form data
            # Redirect to the edit category page with the category ID
            return redirect('edit-category', category_id=category.id)


        else:
            messages.error(request,"jsdjsajsdd")
            # Form is not valid, render the template with the form and errors
            # return render(request, 'create_category.html', {'form': form})
    else:
        form = CategoryForm()
    return redirect('create-category')

def save_book(request):
    resp = { 'status' : 'failed', 'msg':''}

    if request.method == 'POST':
        form = BooksForm(request.POST)
        if form.is_valid():
            book = form.save()  # Save the form data
            # Redirect to the edit category page with the category ID
            return redirect('edit-book', book_id=book.id)


        else:
            messages.error(request,"jsdjsajsdd")
            # Form is not valid, render the template with the form and errors
            # return render(request, 'create_category.html', {'form': form})
    else:
        form = BookForm()
    return redirect('create-book')


# @login_required
# def save_category(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            category = models.Category.objects.get(id = post['id'])
            form = forms.CategoryForm(request.POST, instance=category)
        else:
            form = forms.CategoryForm(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Category has been saved successfully.")
            else:
                messages.success(request, "Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")
    
@login_required
def view_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)
    
    return render(request, 'view_category.html', context)

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
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'edit_category.html', context)



@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    categories= Category.objects.all()
    if request.method == 'POST':
        form = BooksForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('edit-book', book_id=book_id)
    else:
        form = BooksForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'categories': categories
    }
    return render(request, 'edit_book.html', context)



@login_required
def create_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_category'
    context['page_title'] = 'Manage Category'
    
    return render(request, 'create_category.html', context)

@login_required
def delete_category(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Category ID is invalid'
    else:
        try:
            models.Category.objects.filter(pk = pk).delete()
            messages.success(request, "Category has been deleted successfully.")
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


@login_required
def view_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Book.objects.get(id=pk)
    
    return render(request, 'view_book.html', context)

@login_required
def manage_book(request, pk = None):
    categories = Category.objects.all()
    context = context_data(request)
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    context['categories'] = categories
    action = request.GET.get('action')
    if action == 'create':
        context['create'] = 'true'
    else:
        context['create'] = 'false'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Book.objects.get(id=pk)
    return render(request, 'manage_book.html', context)

@login_required
def delete_book(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            models.Book.objects.filter(pk = pk).delete()
            messages.success(request, "Book has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Book Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

