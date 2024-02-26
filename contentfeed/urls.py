from django.urls import path
from . import views

urlpatterns = [
    # Page urls
    path('',views.ContentFeed,{"t_view": 0}, name='home'),
    path('new',views.ContentFeed,{"t_view": 1}, name='newest'),
    path('random',views.ContentFeed,{"t_view": 2}, name='random'),
    path('old',views.ContentFeed,{"t_view": 3}, name='oldest'),
    path('about',views.about,name='about'),
    path('sites',views.sites, name='sites'),
    path('search',views.search, name='search'),
    # Error Pages
    path('404',views.Error404, name='404page'),
    path('500',views.Error500, name='500page'),
    # Function urls
    path('feature/<item_uid>/',views.ItemFeatured,name='feature'),
    path('hide/<item_uid>/',views.ItemHidden,name='hide'),
    path('vote/<uuid:item_id>/<session_id>/',views.Vote,name='vote')
]