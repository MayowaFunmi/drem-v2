from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Category, Comment
from .forms import CategoryForm, CommentForm
from users.decorators import unauthorised_user


def post_list(request):
    all_posts = Post.objects.all().order_by('-date')
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = post.comments.filter(active=True).order_by('-date')

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


"""
class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    login_url = 'users:login'
    
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(post=self.get_object()).order_by('-date')
        data['comments'] = comments_connected

        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(comment=request.POST.get('comment'),
                              author=self.request.user,
                              post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


"""


class PostUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Post
    fields = ('categories', 'title', 'body',)
    template_name = 'blog/post_edit.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        category_list = Category.objects.all()
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['categories'] = [category.name for category in category_list]
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Post
    template_name = 'blog/post_new.html'
    fields = ['categories', 'title', 'body']
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        category_list = Category.objects.all()
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['categories'] = [category.name for category in category_list]
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
@unauthorised_user
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            categories = Category.objects.all()
            context = {
                'categories': categories
            }
            return render(request, 'blog/post_new.html', context)

    else:
        form = CategoryForm()
    return render(request, 'blog/category.html', {'form': form})


@login_required
@unauthorised_user
def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-date'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog/category_post_list.html", context)
