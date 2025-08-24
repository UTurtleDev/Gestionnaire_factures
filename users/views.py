from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()

# Create your views here.
def users(request):
    users_list = User.objects.all().order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users_list, 10)  # 10 utilisateurs par page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'pages/users/users.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur créé avec succès!')
            return redirect('users:users')
    else:
        form = UserCreateForm()
    
    return render(request, 'pages/users/user_create_form.html', {'form': form})


def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'pages/users/user_detail.html', {'user': user})


def user_update(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur modifié avec succès!')
            return redirect('users:detail', pk=user.pk)
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'pages/users/user_update_form.html', {'form': form, 'user': user})


def user_delete(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès!')
        return redirect('users:users')
    
    return render(request, 'pages/users/user_delete.html', {'user': user})