from django.contrib import admin
from contentfeed.models import SourceType, Votes, Publications, ContentItem, PubRequest, ContactRequest

# Register your models here.
admin.site.register(SourceType)
admin.site.register(Votes)
admin.site.register(Publications)

# Customized Views 
#
## Content View
@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display=('item_title','item_votecount','item_curated','item_source','item_datepublished','item_hidden')
    list_filter=['item_source','item_curated','item_hidden']
    actions = ['mark_as_curated','mark_as_uncurated','mark_as_hidden']
    # Methods
    def get_ordering(self, request):
        return ['-item_datepublished']
    
    def mark_as_curated(self, request, queryset):
        queryset.update(item_curated = True)
    mark_as_curated.short_description = "Curate"

    def mark_as_uncurated(self, request, queryset):
        queryset.update(item_curated = False)
    mark_as_uncurated.short_description = "Uncurate"

    def mark_as_hidden(self, request, queryset):
        queryset.update(item_hidden = True)
    mark_as_hidden.short_description = "Hidden"

## Publication Requests
@admin.register(PubRequest)
class PublicationRequestAdmin(admin.ModelAdmin):
    list_display=('pubreq_name','pubreq_url','pubreq_date','pubreq_complete')
    list_filter=['pubreq_complete']
    actions=['mark_as_complete']
    # Methods
    def get_ordering(self, request):
        return ['pubreq_complete','-pubreq_date']
    def mark_as_complete(self, request, queryset):
        queryset.update(pubreq_complete = True)
    mark_as_complete.short_description = "Complete"

## Contact Requests
@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display=('contact_name','contact_email','contact_date','contact_complete')
    list_filter=['contact_complete']
    actions=['mark_as_complete']
    # Methods
    def get_ordering(self, request):
        return ['contact_complete','-contact_date']
    
    def mark_as_complete(self, request, queryset):
        queryset.update(contact_complete = True)
    mark_as_complete.short_description = "Complete"

    