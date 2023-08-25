from django.shortcuts import render, redirect
from books.forms import BooksForm
from books.models import Book

# Create your views here.
def create_book(request):
    if request.method == "POST":
        form = BooksForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        form = BooksForm()
    return render(request,'index.html',{'form': form})

def view(request):
    books = Book.objects.all()
    return render(request,"view.html",{'books':books})

def delete(request, id):
    books = Book.objects.get(id=id)
    books.delete()
    return redirect("/view")
