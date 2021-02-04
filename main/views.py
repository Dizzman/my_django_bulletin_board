from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts import render


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


class BBLoginView(LoginView):
    template_name = 'main/login.html'
