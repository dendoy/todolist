from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import request
from .models import Todo
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

@login_required
def index(request):
    context = {
        'todos': Todo.objects.filter(user=request.user)
    }

    return render(request, 'todo.html', context)
