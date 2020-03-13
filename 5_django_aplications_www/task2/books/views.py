from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
import json
from .forms import BookForm

# Create your views here.
def showBook(request):
    books = Book.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid(): 
            form.save() 
            return HttpResponseRedirect('/')
    else:
        form = BookForm() 
    return render(request, 'books/books.html', locals())
    
@csrf_protect
def ajaxSaveBook(request):
    book = get_object_or_404(Book, pk=request.POST['id'])
    if str(book.version) == request.POST['version']:
        book.comments = request.POST['comments']
        book.version+=1
        book.save()
        return HttpResponse('0')
    else:
        return HttpResponse('1')

@csrf_protect
def ajaxDeleteBook(request):
    book = get_object_or_404(Book, pk=request.POST['id'])
    book.delete()
    return HttpResponse('0')

@csrf_protect
def ajaxGetBook(request):
    book = get_object_or_404(Book, pk=request.POST['id'])
    data = {'comments': book.comments, 'version': book.version}
    return HttpResponse(json.dumps(data))

@csrf_protect
def ajaxChangeWasRead(request):
    book = get_object_or_404(Book, pk=request.POST['id'])
    if str(book.version) == request.POST['version']: # or str(post_version) == '0':
        book.was_read = not book.was_read
        book.version += 1
        book.save()
        data = {'ret': 0}
    else:            
        data = {'ret': 1}
    data['version'] = book.version
    data['wasRead'] = 1 if book.was_read else 0 
    return HttpResponse(json.dumps(data))
