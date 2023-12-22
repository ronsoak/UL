from django.urls import path
from . import views

urlpatterns = [
    #page urls
    path('',views.ContentFeed,{"t_view": 1}, name='trending-feed'),
    path('new',views.ContentFeed,{"t_view": 0}, name='recent-feed'),
    path('about',views.about, name='about-page'),
    path('publications',views.publications, name='publication-page'),
    # #function urls
    # path('itemclicked/<item_uid>/',views.ItemClicked,name='itemclicked'),
    # path('upvote/<item_uid>/',views.ItemUpvote,name='upvote'),
]