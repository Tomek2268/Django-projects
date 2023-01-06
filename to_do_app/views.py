from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Task
from .forms import TaskForm

# Create your views here.
def home(request):
    return render(request,'to_do_app/home.html')

@login_required(login_url='login')
def to_do_list(request,page):
    search_query = ''
    tasks = Task.objects.filter(owner=request.user)
    if request.GET:
        try:
            search_query = request.GET['search']
            tasks = tasks.filter(
                Q(title__icontains=search_query)|
                Q(body__icontains=search_query)
            )
            try:
                task_id = request.GET['task']
                task = Task.objects.get(id=task_id)
                if task.done:
                    task.done = False
                    task.save()
                else:
                    task.done = True
                    task.save()
            except:
                pass
        except:
            task_id = request.GET['task']
            task = Task.objects.get(id=task_id)
            if task.done:
                task.done = False
                task.save()
            else:
                task.done = True
                task.save()

    paginator = Paginator(tasks,5)
    tasks = paginator.page(page)
    context = {'tasks':tasks,
                'paginator':paginator,
                'current_page':page,
                'search_query':search_query}
    return render(request,'to_do_app/to_do_list.html',context)

@login_required(login_url='login')
def create_task(request):
    page = 'create_task'
    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid:
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('to_do_list',1)

    context = {'form':form,'page':page}
    return render(request,'to_do_app/task_form.html',context)

@login_required(login_url='login')
def task(request,pk):
    if request.GET:
        current_page=request.GET['page']
    page = 'task'
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('to_do_list',int(current_page))

    context = {'page':page,
                'form':form,
                'current_page':current_page}
    return render(request,'to_do_app/task_form.html',context)

@login_required(login_url='login')
def delete_task(request,pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('to_do_list',1)
    context = {'object':task.title}
    return render(request,'delete_view.html',context)