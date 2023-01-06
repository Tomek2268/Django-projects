from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

from .utils import send_welcome_email,create_profile
from .forms import RegisterForm,EditUserForm,MessageForm
from .models import Message

# Create your views here.

def login_view(request):
    errors = {}
    username_value = ''
    try:
        if request.GET['next'] and request.method != 'POST':
            messages.warning(request,'Log in to see this page!')
    except:
        pass
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        all_usernames = []
        for user in User.objects.all():
            all_usernames.append(user.username)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You are logged in!')
            return redirect(request.GET['next'] if request.GET else 'home')
        elif username in all_usernames:
            errors['password_error'] = 'Password incorrect!'
            username_value = username
        else:
            errors['username_error'] = 'Username incorrect!'

    context = {'errors':errors,'username_value':username_value}
    return render(request,'users/login.html',context)

def logout_view(request):
    logout(request)
    messages.info(request,'You are logged out.')
    return redirect('login')

def register_view(request):
    page = 'register'
    form = RegisterForm
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            create_profile(user)
            send_welcome_email(user)
            messages.success(request,'User created successfully!')
            login(request,user)
            return redirect('home')

    context = {'form':form,'page':page}
    return render(request,'users/user_form.html',context)

@login_required(login_url='login')
def account(request):
    user = request.user
    context = {'user':user}
    return render(request,'users/profile.html',context)

@login_required(login_url='login')
def edit_account(request):
    page = 'edit'
    user = request.user
    form = EditUserForm(instance=user)
    if request.method == 'POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Info updated successfully!')
            return redirect('account')

    context = {'page':page,'form':form}
    return render(request,'users/user_form.html',context)

@login_required(login_url='login')
def change_password(request):
    errors = {}
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        new_password_confirm = request.POST['new_password_confirm']
        user = authenticate(request,username=request.user,password=current_password)
        if user is not None:
            if new_password == new_password_confirm:
                user.set_password(new_password)
                user.save()
                login(request,user)
                messages.success(request,'Password changed successfully!')
                return redirect('account')
            else:
                errors['new_password_field'] = 'New password did not match confirm password!'
        else:
            errors['current_password_field'] = 'Current password is wrong!'

    context = {'errors':errors}
    print(errors)
    return render(request,'users/change_password.html',context)

@login_required(login_url='login')
def inbox(request,page):
    if request.GET:
        try:
            try:
                message_id = request.GET['message_id']
                message = Message.objects.get(id=message_id)
                message.delete()
            except:
                pass
            request.GET['checked'] == 'on'
            checkbox_value = 'checked'
            user_messages = Message.objects.filter(recipient=request.user,is_read=False)
        except:
            message_id = request.GET['message_id']
            message = Message.objects.get(id=message_id)
            message.delete()
            checkbox_value = ''
            user_messages = Message.objects.filter(recipient=request.user)
    else:
        checkbox_value = ''
        user_messages = Message.objects.filter(recipient=request.user)
    paginator = Paginator(user_messages,5)
    if page != 1:
        if paginator.page(page - 1).has_next() == False:
            page -= 1
    user_messages_paginated = paginator.page(page)
    
    context = {'user_messages':user_messages_paginated,
                'paginator':paginator,
                'current_page':page,
                'checkbox_value':checkbox_value}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def message_form(request,pk,has_recipient):
    form = MessageForm
    sender = request.user
    if has_recipient == 'True':
        recipient = User.objects.get(id=pk)

    if request.method =="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            if has_recipient == 'True':
                message.recipient = recipient
            message.save()
            messages.success(request,'Message sent successfully!')
            return redirect('inbox',1)

    context = {'form':form,'has_recipient':has_recipient}
    return render(request,'users/message_form.html',context)

@login_required(login_url='login')
def single_message(request,pk):
    message = Message.objects.get(id=pk)
    if request.GET['page']:
        page = request.GET['page']
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message,'page':page}
    return render(request,'users/single_message.html',context)

@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        messages_num = Message.objects.filter(recipient=request.user).count()
        same_num_of_pages = messages_num % 5
        if same_num_of_pages != 0:
            return redirect('inbox',int(request.GET['page']))
        elif request.GET['page'] == '1':
            return redirect('inbox',1)
        else:
            return redirect('inbox',int(request.GET['page']) - 1)
    context = {'object':message.title}
    return render(request,'delete_view.html',context)