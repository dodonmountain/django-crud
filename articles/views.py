from django.shortcuts import render
from .models import Article
# Create your views here.
def index(request):
    articles = Article.objects.all()
    titles = []
    contents = []
    for i in articles:
        titles.append(i.title)
        contents.append(i.content)

    context = {
        'articles': articles,
        'titles' : titles,
        'contents' : contents,
    }
    return render(request, 'articles/index.html', context)