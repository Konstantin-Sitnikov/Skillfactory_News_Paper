from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


from .forms import Publication
from .models import Post, Comment, Author, Category
from .filters import NewsFilter



class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 15



class PostSearch(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        print(context['filterset'])
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        publication = self.get_object()
        context = super().get_context_data(**kwargs)
        context['update_news'] = (publication.type == "NW")
        context['update_article'] = (publication.type == "AR")
        context['comments'] = Comment.objects.filter(post_id=publication.pk)

        return context


class PublicationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = Publication
    model = Post
    template_name = 'news/create_publication.html'

    def form_valid(self, form):
        publication = form.save(commit=False)
        author = Author.objects.get(user=self.request.user)

        print(author.post_count)

        if author.post_count < 3:
            if self.request.path == "/news/create/":
                publication.autor_id = author
                publication.type = "NW"
                author.get_count()
                return super().form_valid(form)
    
            if self.request.path == "/article/create/":
                publication.autor_id = author
                publication.type = "AR"
                author.get_count()
                return super().form_valid(form)
        else:
            message = 'Количество публикаций на сегодня закончено'
            return render(self.request, 'news/publication_creation_error.html', {'message': message})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(user=self.request.user)
        context['create_news'] = (self.request.path == "/news/create/")
        context['create_article'] = (self.request.path == "/article/create/")
        context['null_publication'] = author.post_count > 3
        return context


class PublicationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = Publication
    model = Post
    template_name = 'news/create_publication.html'

    def form_valid(self, form):
        publication = form.save(commit=False)
        if publication.type == "NW" and self.request.path == f"/news/{publication.pk}/edit/":
            return  super().form_valid(form)
        elif publication.type == "AR" and self.request.path == f"/article/{publication.pk}/edit/":
            return  super().form_valid(form)
        else:
            return redirect("edit_delete_error")



class PublicationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/publication_delete.html'
    success_url = reverse_lazy('news_list')


def edit_delete_invalid(request):
    return HttpResponse("Ошибочка! Неверный путь!")


def like_dislike(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get("like") == "like":
            post.like()
            post.save()
            return redirect("news_detail", pk)
        elif request.POST.get("dislike") == "dislike":
            post.dislike()
            post.save()
            return redirect("news_detail", pk)



class CategoryList(PostList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'

    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы отписались от категории'

    return render(request, 'news/subscribe.html', {'category': category, 'message': message})

@login_required
def create_comment(request, pk):
    if request.method == "POST":
        comment = Comment(post_id=Post.objects.get(pk=pk), user_id=request.user, text_comment=request.POST.get("text"))
        comment.save()
        return redirect("news_detail", pk)
