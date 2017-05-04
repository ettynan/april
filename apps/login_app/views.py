from django.shortcuts import render, redirect, HttpResponse
from . models import User
from django.contrib import messages

# Create your views here.

def index(request):
    print 'a'
    context = {
        'users': User.objects.all()
    }
    return render(request, 'login_app/index.html', context)

def process(request):
    print 'b', request.POST
    # request.POSt to models. models sharpie it label data
    valid, errors = User.objects.validate_user(request.POST) 

    if valid: #if they have followed all the rules and it validates, it will allow them forward
        print valid, errors
        request.session.first_name = errors.first_name
        # context = {
        #     'users':User.objects.all()
        # }
        return render(request, 'login_app/success.html')

    else: #if they have any validation errors they cannot move forward
        for error in errors:
            messages.error(request, error)
    return redirect('/')

def login(request):
    print 'c'
    valid, errors = User.objects.validate_login(request.POST)
    if valid is True: #if they have followed all the rules and it validates, will move forward
        print valid, errors
        request.session.first_name = errors.first_name
        # context = {
        #     'users':User.objects.all()
        # }
        return render(request, 'login_app/success.html')

    else: #if they have any validation errors they cannot move forward
        for error in errors:
            messages.error(request, error)
        return redirect('/')

def remove(request, id):
    print 'd'
    if request.method == "POST":
        User.objects.filter(id=id).delete()
    return redirect('/login')

def clear(request):
    request.session.clear()
    return redirect('/')
