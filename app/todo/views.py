from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import request
from .models import Todo
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from .forms import TodoForm


class Home(TemplateView):
    template_name = 'home.html'

@login_required
def index(request):
    context = {
        'todos': Todo.objects.filter(user=request.user),
        'form':  TodoForm()
    }
    return render(request, 'todo.html', context)

@login_required
@require_POST
def submit_todo(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()

        #return an html partial
        context = {'todo': todo}
        return render(request, 'todo.html#todoitem-partial', context)
