from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django import VERSION

from .forms import UserRegistrationForm, UserEditForm


def home(request):
    """Home page view"""
    context = {
        'django_version': f'{VERSION[0]}.{VERSION[1]}.{VERSION[2]}'
    }
    return render(request, 'home.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def admin_required(view_func):
    """Decorator to check if user is admin (staff)"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, '您没有权限访问此页面')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def user_list(request):
    """User list view with pagination and search"""
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    users = User.objects.all().order_by('-date_joined')

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(users, 10)  # 10 users per page
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_users': paginator.count,
    }
    return render(request, 'accounts/user_list.html', context)


@login_required
@admin_required
def user_detail(request, user_id):
    """User detail view"""
    user_obj = get_object_or_404(User, id=user_id)
    context = {
        'user_obj': user_obj,
    }
    return render(request, 'accounts/user_detail.html', context)


@login_required
@admin_required
def user_edit(request, user_id):
    """Edit user view (admin only)"""
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'用户 {user_obj.username} 更新成功')
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user_obj)

    context = {
        'form': form,
        'user_obj': user_obj,
    }
    return render(request, 'accounts/user_edit.html', context)


@login_required
@admin_required
def user_delete(request, user_id):
    """Delete user view (admin only)"""
    user_obj = get_object_or_404(User, id=user_id)

    if user_obj.id == request.user.id:
        messages.error(request, '不能删除自己的账号')
        return redirect('user_list')

    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f'用户 {username} 已删除')
        return redirect('user_list')

    context = {
        'user_obj': user_obj,
    }
    return render(request, 'accounts/user_delete.html', context)