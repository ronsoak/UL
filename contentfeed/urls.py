from django.urls import path
from . import views

urlpatterns = [
    #page urls
    path('',views.ContentFeed,{"t_view": 0}, name='trending'),
    path('new',views.ContentFeed,{"t_view": 1}, name='newest'),
    path('random',views.ContentFeed,{"t_view": 2}, name='random'),
    path('old',views.ContentFeed,{"t_view": 3}, name='oldest'),
    path('about',views.about,name='about'),
    path('sources',views.sources, name='sources'),
    path('search',views.search, name='search'),
    # redesign
    path('home',views.CFEED,{"t_view": 0}, name='home2'),
    path('new2',views.CFEED,{"t_view": 1}, name='new2'),
    path('rand2',views.CFEED,{"t_view": 2}, name='rand2'),
    path('old2',views.CFEED,{"t_view": 3}, name='old2'),
    path('about2',views.about2,name='about2'),
    path('sources2',views.sources2, name='sources2'),
    path('search2',views.search2, name='search2'),
    #function urls
    path('itemclicked/<item_uid>/',views.ItemClicked,name='itemclicked'),
    path('upvote/<item_uid>/',views.ItemUpvote,name='upvote'),
]