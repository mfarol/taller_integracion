from django.urls import path

from . import views

app_name = 'rick'
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:item_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('character/<int:character_id>', views.character, name='character'),
    path('location/<int:location_id>', views.location, name='location'),
    path('search/', views.search, name='search'),
]
