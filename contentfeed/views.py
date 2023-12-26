from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from contentfeed.forms import NewContactForm, NewSourceForm
from contentfeed.models import ContentItem, Publications, Votes
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# -- -- -- -- -- -- PAGE RENDERERS -- -- -- -- -- -- -- #

# About Page

def about(request):
    cform = NewContactForm(request.POST or None )
    if cform.is_valid():
        cform.save()
        return HttpResponseRedirect("/about")
    else:
        pass 
    return render(request, 'about.html', context={"NewContactRequest": cform})

# Home Page i.e Content Feed
def ContentFeed(request,t_view):
    '''Home Page for Website showing Trending and Curated Items'''
    t = t_view
    datestart = date.today()
    dateend = datestart - timedelta (days=30)
    page = request.GET.get("page")
    qlimit =  100
    plimit = 25
    #
    if t != 1:
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('-item_datepublished')[:qlimit]
    else:
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
        "t_flag": t,
        "plimit": plimit
    }
    return render(request,'feed.html',context)

# Publications Page
def publications(request):
    # Publication Query
    pub_query = Publications.objects.filter(pub_hidden=False)
    # User Form
    sform = NewSourceForm(request.POST or None )
    if sform.is_valid():
        sform.save()
        return HttpResponseRedirect("/publications")
    else:
        pass
    return render(request, 'publications.html',context={"NewSourceRequest": sform,"publications":pub_query})

# -- -- -- -- -- -- PAGE FUNCTIONS -- -- -- -- -- -- -- #

def ItemClicked(request,item_uid):
    u = ContentItem.objects.get(item_id = item_uid).item_url
    session_id = request.session.session_key
    VoteForItem(item_uid,session_id)
    return redirect (u)

def ItemUpvote(request,item_uid):
    session_id = request.session.session_key
    VoteForItem(item_uid,session_id)
    return redirect('/')

def VoteForItem(item_uid,session_id):
    i = ContentItem.objects.get(item_id = item_uid)
    s = session_id
    can_vote = 0
    if Votes.objects.filter(vote_id=item_uid,session_id=session_id).exists():
        can_vote = 0 
    else:
        can_vote = 1
    if can_vote == 1:
        i.item_votecount = i.item_votecount + 1
        i.save()
        new_vote=Votes(vote_id = item_uid, session_id = session_id)
        new_vote.save()
