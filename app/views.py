from hashids import Hashids
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import LinkForm
from .models import Link


class ShortenLinkView (View):

    def get(self, request):
        return render(request, 'links/home.html', context={'form': LinkForm()})


    def post(self, request):
        form = LinkForm(request.POST)
        if form.is_valid():
            user_link = form.cleaned_data['user_link']
            if Link.objects.filter(full_link=user_link).exists(): #если ссылка есть в бд, возвращаем ее
                bd_link = Link.objects.get(full_link=user_link)
                text = f'http://127.0.0.1:8000/{bd_link.short_link}'
                return render(request,
                              'links/home.html',
                              context={'form': LinkForm(), 'text': text, 'full_link': user_link})
            id = Link.objects.all().count()    #если нет, создаем токен по номеру записи в бд
            hashids = Hashids(min_length=6)
            hashid = hashids.encode(id)
            text = f'http://127.0.0.1:8000/{hashid}'
            link_object = Link(full_link=user_link, short_link=hashid, user=request.user)
            link_object.save()
            return render(request,
                          'links/home.html',
                          context={'form': LinkForm(), 'text': text, 'full_link': user_link})
        else:
            return HttpResponse('kl')


class RedirectShortURL(View):

    def get(self, request, hashid):
        print(hashid)
        link = get_object_or_404(Link, short_link=hashid)
        return redirect(link.full_link)


class HistoryView(View):

    def get(self, request):
        links = Link.objects.filter(user=request.user)
        return render(request, 'links/history.html', context={'links': links})



#todo хэш функция, сделать поле ссылки уникальным
