import django
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)
from .models import *
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = 'You have to be logged in to access that page'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You need to login to access This Page.', 'danger')
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


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

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Comment.objects.create(
                user=request.user,
                post=Post.objects.get(id=self.kwargs['pk']),
                comment=request.POST.get('commet')
            )
            return redirect(f'/post/{self.kwargs["pk"]}')
        messages.error(request, 'You need to login to access This Page.', 'danger')
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['pk']).all()
        context['images'] = PostImages.objects.filter(post_id=self.kwargs['pk']).all()
        return context


class UserPostListlView(ListView):
    model = Post

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, id=self.kwargs.get('pk'))
        return context


@login_required
def post_create_view(request):
    if request.method == "POST":
        p_form = PostCreateForm(request.POST)
        p_form.instance.author = request.user
        # i_form = PostImageCreateForm(request.FILES)
        p_form.save()
        images = request.FILES.getlist('images')
        for image in images:
            PostImages.objects.create(image=image, post=p_form.instance)
        return redirect('blog-home')
    else:
        p_form = PostCreateForm(instance=request.user)
    images = PostImages.objects.all()
    context = {'form': p_form, 'images': images}
    return render(request, 'blog/post_create_view.html', context)


# LoginRequiredMixin 相当于@login_required
# class PostCreateView(CustomLoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content', 'post_image']
#
#     def form_valid(self, form):
#         # 提交的表单对应的post(instance)的作者必须是当前登录的作者
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# UserPassesTestMixin 检查修改post的用户是否是author
class PostUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'latex']

    def form_valid(self, form):
        # 检验
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()  # 获得当前修改的post对象
        # 检验当前登录用户是否是post的用户
        if self.request.user == post.author:
            return True
        return False

    # 如果不加会导致post没有author，报错
    # 确定修改post的用户是否是创建post的用户


class PostImageListView(CustomLoginRequiredMixin, ListView):
    model = PostImages
    fields = '__all__'

    def get_queryset(self):
        return PostImages.objects.filter(post=self.kwargs.get('pk')).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('pk')
        return context


class PostImageCreateView(CustomLoginRequiredMixin, CreateView):
    model = PostImages
    fields = ['image']

    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.post = post
        return super().form_valid(form)


class PostImageUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = PostImages
    fields = ['image']

    def form_valid(self, form):
        # 检验
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostImageDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = PostImages

    def get_success_url(self):
        # return reverse('postimages', kwargs={'pk':self.kwargs.get('pk')})
        return self.object.get_absolute_url()


class PostDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
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


class CommentDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

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

    # 设置删除成功之后redirect的网页，没有会报错
    # success_url = '/'


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)
