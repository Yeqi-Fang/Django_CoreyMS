from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def my_login_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            func(request, *args, **kwargs)
        messages.error(request, 'You need to login to access This Page.', 'danger')
        return redirect('/login/')

    return inner


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# @my_login_required
@login_required
def profile(request):
    if request.method == 'POST':

        # 将用户post的数据存入form中，再将其绑定到当前登录的user中.instance是为了确定要更新的实例
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # 接受files文件
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        # instance指的是form绑定的model(在这里指的是user)，用于填充email和profile.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
