import django
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # 基于对象的View默认的html地址
    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    fields = ['title', 'content', 'post_image']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commets'] = Comment.objects.filter(post_id=self.kwargs['pk']).all()
        return context


# LoginRequiredMixin 相当于@login_required
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        # 提交的表单对应的post(instance)的作者必须是当前登录的作者
        form.instance.author = self.request.user
        return super().form_valid(form)


# UserPassesTestMixin 检查修改post的用户是否是author
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # 如果不加会导致post没有author，报错
    def form_valid(self, form):
        # 检验
        form.instance.author = self.request.user
        return super().form_valid(form)

    # 确定修改post的用户是否是创建post的用户
    def test_func(self):
        post = self.get_object()  # 获得当前修改的post对象
        # 检验当前登录用户是否是post的用户
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # 设置删除成功之后redirect的网页，没有会报错
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        try:
            if self.request.user == post.author or self.request.user.is_superuser:
                return True
            return False
        except django.contrib.auth.models.User.DoesNotExist:
            if self.request.user.is_superuser:
                return True
            return False
    # def


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    # 设置删除成功之后redirect的网页，没有会报错
    # success_url = '/'

    def test_func(self):
        comment = self.get_object()
        try:
            if self.request.user == comment.user or self.request.user == comment.post.author or self.request.user.is_superuser:
                return True
            return False
        except django.contrib.auth.models.User.DoesNotExist:
            if self.request.user.is_superuser:
                return True
            return False

    def get_success_url(self):
        return self.object.get_absolute_url()


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def commet(request, pk):
    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            post=Post.objects.get(id=pk),
            commet=request.POST.get('commet')
        )
        return redirect(f'/post/{pk}')
# def CommentCreateView(ListView):
