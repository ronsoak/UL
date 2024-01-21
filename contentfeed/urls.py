from django.urls import path
from . import views

urlpatterns = [
    #page urls
    path('',views.ContentFeed,{"t_view": 0}, name='home'),
    path('new',views.ContentFeed,{"t_view": 1}, name='newest'),
    path('random',views.ContentFeed,{"t_view": 2}, name='random'),
    path('old',views.ContentFeed,{"t_view": 3}, name='oldest'),
    path('about',views.about,name='about'),
    path('sites',views.sources, name='sites'),
    path('search',views.search, name='search'),
    #function urls
    path('itemclicked/<item_uid>/',views.ItemClicked,name='itemclicked'),
    path('upvote/<item_uid>/',views.ItemUpvote,name='upvote'),
]