from django.urls import path
from . import views

urlpatterns = [
    #page urls
    path('',views.ContentFeed,{"t_view": 0}, name='trending'),
    path('new',views.ContentFeed,{"t_view": 1}, name='newest'),
    path('random',views.ContentFeed,{"t_view": 2}, name='random'),
    path('old',views.ContentFeed,{"t_view": 3}, name='oldest'),
    path('about',views.about, name='about'),
    path('publications',views.publications, name='publications'),
    #function urls
    path('itemclicked/<item_uid>/',views.ItemClicked,name='itemclicked'),
    path('upvote/<item_uid>/',views.ItemUpvote,name='upvote'),
]