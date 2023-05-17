from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import resolve
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, BaseRegisterForm, Mailing, Category
from .filters import NewsFilter
from NewsPaper.forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-time']

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['total'] = Post.objects.all().count
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostListFiltered(ListView):
    model = Post
    template_name = 'post/search.html'
    context_object_name = 'post_list_filtered'
    ordering = ['-time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.change_post',)

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs.get('pk'))
    

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('post.delete_post',)
    

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class PostCategoryView(ListView):
    model = Post
    template_name = 'post/category.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCategory=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category
        return context

@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mailing/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Подписка на {category} на сайте News Paper',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))
        #return redirect('news_list')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))

class MailingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'post/make_app.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Mailing(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        return redirect('news:make_app')