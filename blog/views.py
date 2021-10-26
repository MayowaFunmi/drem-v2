from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Post, Category, Comment
from .forms import CategoryForm, CommentForm
from users.decorators import unauthorised_user


def post_list(request):
    all_posts = Post.objects.all().order_by('-updated_on')
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'latest_post': all_posts[0].title
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = post.comments.filter(active=True).order_by('-updated')
    new_comment = None
    liked = False
    if post.likes.filter(id=request.user.id).exists:
        liked = True
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
        'liked': liked
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        user_category = request.POST['category']
        title = request.POST['title']
        body = request.POST['body']

        t_str = title.lower()
        for i in range(0, len(t_str), 1):
            if t_str[i] == ' ':
                t_str = t_str.replace(t_str[i], '-')

        category = Category.objects.get(name=user_category)

        new_post = Post.objects.create(author=request.user, slug=t_str, title=title, body=body)
        new_post.save()
        new_post.categories.add(category)
        return redirect('/blog/')

    context = {
        'categories': categories
    }
    return render(request, 'blog/post_new.html', context)


@login_required
def post_edit(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)

    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        post.title = title
        post.body = body
        post.save()
        return redirect('/blog/')

    context = {
        'post': post
    }
    return render(request, 'blog/post_edit.html', context)


@login_required
def post_delete(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.method == 'POST':
        ask = request.POST['ask']
        if ask == 'Yes':
            post.delete()
            return redirect('/blog/')
        elif ask == 'No':
            return redirect('/blog/')
    return render(request, 'blog/post_delete.html', {'post': post})


def like_view(request, id, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'), slug=slug)
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:post_detail', args=[int(id), str(slug)]))


"""
def like_view(request, id, slug):
    #liked = False
    if request.method == 'POST':
        post = get_object_or_404(Post, id=request.POST.get('post_id'), slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            #liked = False
        else:
            post.likes.add(request.user)
            #liked = True

    return HttpResponseRedirect(reverse('blog:post_detail', args=[int(id), str(slug)]))

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
"""


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
