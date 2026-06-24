from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import CadastroForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/admin/')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        next_url = request.GET.get('next', '/admin/')
        return redirect(next_url)

    return render(request, 'login.html', {'form': form})


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('/admin/')

    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/admin/')

    return render(request, 'cadastro.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logout_confirm.html')
