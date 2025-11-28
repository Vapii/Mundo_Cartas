from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from .forms import RegistroForm, LoginForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            grupo_usuario, creado = Group.objects.get_or_create(name='user')
            usuario.groups.add(grupo_usuario)

            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'usuario/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'usuario/login.html', {'form': form})


