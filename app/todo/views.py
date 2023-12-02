from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Todo
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST, require_http_methods
from .forms import TodoForm
from django.http import HttpResponse


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
    
@login_required
@require_POST
def complete_todo(request,pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_completed =True
    todo.save()
    context = {'todo':todo}
    return render(request,'todo.html#todoitem-partial', context)


@login_required
@require_http_methods('DELETE')
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'delete-todo'
    return response