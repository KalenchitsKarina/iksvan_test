from django.urls import path

from .views import ShortenLinkView, RedirectShortURL, HistoryView

urlpatterns = [
    path('', ShortenLinkView.as_view(), name='home'),
    path('history/', HistoryView.as_view(), name='history'),
    path('<str:hashid>/', RedirectShortURL.as_view()),
]
