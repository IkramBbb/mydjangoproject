from django.shortcuts import render, redirect
from .models import News, Category
from news.forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'ib519500@gmail.com', ['ikramsarsenbaev@yandex.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error('Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})


class HomeNews(ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная Страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


# class CreateNews(LoginRequiredMixin, CreateView):
#     form_class = NewsForm
#     template_name = 'news/add_news.html'
#     # success_url = reverse_lazy('home')
#     raise_exception = True
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user.username
#         return super().form_valid(form)


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            # news = News.objects.create(**form.cleaned_data)
            news = form.save(commit=False)
            news.username = request.user
            form.save()
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
