from hashids import Hashids
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import LinkForm
from .models import Link


MY_DOMAIN = 'http://kkalen9c.beget.tech/'


class ShortenLinkView (View):

    def get(self, request):
        return render(request, 'links/home.html', context={'form': LinkForm()})

    def post(self, request):
        form = LinkForm(request.POST)
        if form.is_valid():
            user_link = form.cleaned_data['user_link']
            if Link.objects.filter(full_link=user_link).exists():         #если ссылка есть в бд, возвращаем ее
                bd_link_object = Link.objects.get(full_link=user_link)
                bd_link_object.users.add(request.user)                  #связываем ссылку с текущим пользователем
                short_link = MY_DOMAIN + bd_link_object.short_link
            else:
                id = Link.objects.all().count()                     #если нет, создаем токен по номеру записи в бд
                hashids = Hashids(min_length=6)
                hashid = hashids.encode(id)
                short_link = MY_DOMAIN + hashid
                link_object = Link(full_link=user_link, short_link=hashid)
                link_object.save()
                link_object.users.add(request.user)

            return render(request,
                          'links/home.html',
                          context={'form': LinkForm(), 'short_link': short_link, 'full_link': user_link})
        else:
            return HttpResponse('kl')
#todo fix else

class RedirectShortURL(View):

    def get(self, request, hashid):
        link = get_object_or_404(Link, short_link=hashid)
        return redirect(link.full_link)


class HistoryView(View):

    def get(self, request):
        links = Link.objects.filter(users=request.user)
        return render(request, 'links/history.html', context={'links': links})




