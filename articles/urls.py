from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static 
app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail,name='detail'),
    path('<int:article_pk>/delete', views.delete,name='delete'),
    path('<int:article_pk>/update', views.update,name='update'),
    path('<int:article_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/<int:comment_id>/comment_delete/', views.comment_delete, name='comment_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)