from datetime import date, timedelta
from django.shortcuts import render
from contentfeed.models import ContentItem
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# About Page

def about(request):
    # sform = NewSourceForm(request.POST or None )
    # cform = NewContactForm(request.POST or None )
    # # New Source Form
    # if sform.is_valid():
    #     sform.save()
    #     return HttpResponseRedirect("/about")
    # else:
    #     pass
    # # New Contact Form 
    # if cform.is_valid():
    #     cform.save()
    #     return HttpResponseRedirect("/about")
    # else:
    #     pass 
    #return render(request,'about.html',context={"NewSourceRequest": sform,"NewContactRequest": cform})
    return render(request, 'about.html')

# Home Page i.e Content Feed
def ContentFeed(request,t_view):
    '''Home Page for Website showing Trending and Curated Items'''
    t = t_view
    datestart = date.today()
    dateend = datestart - timedelta (days=30)
    page = request.GET.get("page")
    qlimit =  100
    #
    if t != 1:
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('-item_datepublished')[:qlimit]
    else:
        content_query = ContentItem.objects.filter(item_datepublished__range=[dateend,datestart],item_hidden=False).order_by('-item_votecount','-item_datepublished')[:qlimit]
    
    paginator = Paginator(content_query,25)
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
        "t_flag": t
    }
    return render(request,'feed.html',context)

# Publications Page
def publications(request):
    return render(request, 'publications.html')