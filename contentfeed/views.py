from datetime import date, timedelta
from sys import stdout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from contentfeed.forms import NewContactForm, NewSourceForm
from contentfeed.models import ContentItem, Publications, Votes
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db.models import Q

# -- -- -- -- -- -- PAGE RENDERERS -- -- -- -- -- -- -- #
# About Page
def about(request):
    cform = NewContactForm(request.POST or None )
    f_valid = 0
    if request.method == "POST":
        if cform.is_valid():
            cform.save()
            f_valid = 1
            cform = NewContactForm()
            return render(request,'about.html', context={"fvalid":f_valid})
        else:
            f_valid = 2 
    return render(request, 'about.html', context={"NewContactRequest": cform, "fvalid":f_valid})

# Home Page i.e Content Feed
def ContentFeed(request,t_view):
    '''Home Page for Website showing Trending and Curated Items'''
    t = t_view
    datestart = date.today()
    dateend = datestart - timedelta (days=90)
    page = request.GET.get("page")
    qlimit =  99
    plimit = 25
    if t == 1:      # 1 = Newset
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('-item_datepublished')[:qlimit]
    elif t == 2:    # 2 = Random
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('?')[:qlimit]
    elif t == 3:    # 3 = Oldest
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('item_datepublished')[:qlimit]
    else:           # 0 = Trending (Default)
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('-item_votecount','-item_datepublished')[:qlimit]
    
    paginator = Paginator(content_query,plimit)
    curated = ContentItem.objects.filter(item_curated=True,item_hidden=False).order_by('-item_datepublished')[:3] #Curated top 3
    page_obj = paginator.get_page(page)
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    context = {
        "content_items": content,
        "curated_items" : curated,
        "page_obj": page_obj,
        "t_view": t,
        "plimit": plimit
    }
    return render(request,'feed.html',context)

# Publications Page
def sites(request):
    # Publication Query
    pub_query = Publications.objects.filter(pub_hidden=False)
    # User Form
    sform = NewSourceForm(request.POST or None )
    f_valid = 0
    if request.method == "POST":
        if sform.is_valid():
            sform.save()
            f_valid = 1
            sform = NewSourceForm()
            return render(request, 'sites.html',context={"NewSourceRequest": sform,"publications":pub_query,"fvalid":f_valid})
        else:
            f_valid = 2
    return render(request, 'sites.html',context={"NewSourceRequest": sform,"publications":pub_query,"fvalid":f_valid})

# Search Page
def search(request):
    # Search results model
    if request.method == "POST":
        squery = request.POST.get('Search Terms', None)
        if squery:
            qlimit = 500
            results = ContentItem.objects.filter(Q(item_title__icontains=squery, item_hidden = False) | Q(item_source__pub_name__icontains=squery)).order_by('-item_datepublished')[:qlimit]
            return render(request, 'search.html', {"results":results})
    return render(request, 'search.html')

# -- -- -- -- -- -- PAGE FUNCTIONS -- -- -- -- -- -- -- #
def ItemClicked(request,item_uid):
    u = ContentItem.objects.get(item_id = item_uid).item_url
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session_id = request.session.session_key
    VoteForItem(item_uid,session_id)
    return redirect (u)

def ItemUpvote(request,item_uid):
    stdout.write("Upvote Started:" + item_uid)
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session_id = request.session.session_key
    VoteForItem(item_uid,session_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ItemFeatured(request,item_uid):
    if request.user.is_authenticated: 
        c = ContentItem.objects.get(item_id = item_uid)
        c.item_curated = True 
        c.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def ItemHidden(request,item_uid):
    if request.user.is_authenticated: 
        c = ContentItem.objects.get(item_id = item_uid)
        c.item_hidden = True 
        c.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def VoteForItem(item_uid,session_id):
    c = ContentItem.objects.get(item_id = item_uid)
    i = item_uid
    s = session_id
    can_vote = 0
    if Votes.objects.filter(item_id=i,session_id=s).exists():
        can_vote = 0 
    else:
        can_vote = 1
    if can_vote == 1:
        c.item_votecount = c.item_votecount + 1
        c.save()
        new_vote=Votes(item_id=i, session_id = s)
        new_vote.save()