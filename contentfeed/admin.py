from django.contrib import admin
from contentfeed.models import SourceType, Votes, Publications, ContentItem, PubRequest, ContactRequest

# Register your models here.
admin.site.register(SourceType)
admin.site.register(Votes)
admin.site.register(Publications)

# Customised Views 
#
## Content View
@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display=('item_title','item_votecount','item_curated','item_source','item_datepublished','item_hidden')
    
    def get_ordering(self, request):
        return ['-item_datepublished']

## Publication Requests
@admin.register(PubRequest)
class PublicationRequestAdmin(admin.ModelAdmin):
    list_display=('pubreq_name','pubreq_url','pubreq_date','pubreq_complete')

    def get_ordering(self, request):
        return ['pubreq_complete','-pubreq_date']

## Contact Requests
@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display=('contact_name','contact_email','contact_date','contact_complete')

    def get_ordering(self, request):
        return ['contact_complete','-contact_date']

