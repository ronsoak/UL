from datetime import date, timedelta
from sys import stdout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from contentfeed.forms import NewContactForm, NewSourceForm
from contentfeed.models import ContentItem, Publications, Votes
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
# -- -- -- -- -- -- PAGE RENDERERS -- -- -- -- -- -- -- #
# About Page
def about(request):
    cform = NewContactForm(request.POST or None )
    f_valid = 0
    if request.method == "POST":
        if cform.is_valid():
            cform.save()
            f_valid = 1
            subject = '[Reconnect] New Contact Request'
            message = 'Please log into the site to see the new contact request'
            from_email = 'christian_a_young@icloud.com'
            recipient_list = ['alex@antranaut.com']
            send_mail(subject, message, from_email, recipient_list)
            cform = NewContactForm()
            return render(request,'about.html', context={"fvalid":f_valid})
        else:
            f_valid = 2 
    return render(request, 'about.html', context={"NewContactRequest": cform, "fvalid":f_valid})

# Home Page i.e Content Feed
@csrf_protect
def ContentFeed(request,t_view):
    '''Home Page for Website showing Trending and Curated Items'''
    t = t_view
    datestart = date.today()
    dateend = datestart - timedelta (days=90)
    page = request.GET.get("page")
    qlimit =  99
    plimit = 25
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session_id = request.session.session_key
    if t == 1:      # 1 = Newset
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).select_related("item_source").order_by('-item_datecreated')[:qlimit]
    elif t == 2:    # 2 = Random
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).select_related("item_source").order_by('?')[:qlimit]
    elif t == 3:    # 3 = Oldest
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).select_related("item_source").order_by('item_datepublished')[:qlimit]
    else:           # 0 = Trending (Default)
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).select_related("item_source").order_by('-item_votecount','-item_datepublished')[:qlimit]
    
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
        "plimit": plimit,
        "session_id": session_id,
    }
    return render(request,'feed.html',context)

# Publication Lookup
def PublicationLookup(request,pubid):
    pub_query = ContentItem.objects.filter(item_source=pubid,item_hidden=False).order_by('-item_datepublished')[:1000]
    pub_detail = Publications.objects.filter(pub_id=pubid,pub_hidden=False)
    pub_list = Publications.objects.filter(pub_hidden=False)
    context = {
        "pub_items": pub_query,
        "pub_detail": pub_detail,
        "pub_list" : pub_list
    }
    return render(request,'publist.html',context)

# Sites Page
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
            # email stuff 
            subject = '[Reconnect] New Pub Request'
            message = 'Please log into the site to see the new pub request'
            from_email = 'christian_a_young@icloud.com'
            recipient_list = ['alex@antranaut.com']
            send_mail(subject, message, from_email, recipient_list)
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

def Vote(self,item_id,session_id):
    i = item_id
    s = session_id
    can_vote = 0 
    if Votes.objects.filter(item_id=i,session_id=s).exists():
        can_vote = 0
        return HttpResponse('User has already voted for this item.')
    else:
        can_vote = 1
    if can_vote == 1:
        c = ContentItem.objects.get(item_id = i)
        c.item_votecount = c.item_votecount + 1
        c.save()
        new_vote = Votes(item_id=i,session_id=s)
        new_vote.save()
        return HttpResponse('Vote Successful')
    
def Error404(request):
    return render(request, '404.html')

def Error500(request):
    return render(request, '500.html')