from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .models import AdvUser
from .forms import ChangeUserInfoForm


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя успешно изменен!'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Контроллер странницы основных данных, который выполняет правку записи модели AdvUser"""
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        """Получение  ключа текущего пользователя( выполняется в начале исполнения контроллера-класса)"""
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Извлечение исправляемой записи"""
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def index(request):
    """Тестовая стартовая страница"""
    return render(request, 'main/index.html')


def other_page(request, page):
    """Страница со сведениями о сайте"""
    try:
        # пытаемся загрузить полный путь к нужному шаблону
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    return render(request, 'main/profile.html')
