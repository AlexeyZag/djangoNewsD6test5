from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Post, User, Category
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, CategoryForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


class CategoryAdd(CreateView):
    template_name = 'subscribe.html'
    model = Category
    queryset = Category.objects.all()
    form_class = CategoryForm


    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(User.objects.get(username=str(user)))
        return redirect('/')
class CategoryRemove(CreateView):
    template_name = 'unsubscribe.html'
    model = Category
    queryset = Category.objects.all()
    form_class = CategoryForm

    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.remove(User.objects.get(username=str(user)))
        return redirect('/')
class AddProtectedView(PermissionRequiredMixin, CreateView):
    template_name = 'add_article.html'
    form_class = PostForm
    login_url='/accounts/login'
    permission_required = ('news.add_post')
    model = Post
    queryset = Post.objects.all()

    def form_valid(self, form):
        self.object = form.save(commit= False)
        author = self.request.user
        id = Author.objects.get(author= User.objects.get(username = author)).id
        self.object.author_id = id
        self.object.save()
        return  super().form_valid(form)

class AuthorsList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    queryset = Author.objects.order_by('-id')

class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context


class PostDetail(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        user = self.request.user
        context['post_categories'] = Post.objects.get(pk=id).categories.all()
        context['user_categories'] = Category.objects.filter(subscribers= User.objects.get(username=str(user)))
        return context

"""@login_required
def upgrade_me(request):
    user = request.user
    tag = request.path_info
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(author=User.objects.get(username=user))
    return redirect('/')"""
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'add_article.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post')

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SearchDetail(DetailView):
    model = Post
    template_name = 'search_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()








