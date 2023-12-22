from tabnanny import verbose
import uuid                         # needed for keys
from django.db import models        # standard
from django.utils import timezone   # needed for time delta 

# Source Type (i.e. RSS)
class SourceType(models.Model):
    # Fields 
    type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this content source type", verbose_name="Type Id" )
    type_name = models.CharField(max_length=256,blank=False,null=False, help_text="The name of the source type i.e RSS", verbose_name="Type Name")
    type_hidden = models.BooleanField(default=False, help_text="A flag to determine whether this item should be hidden from the site", verbose_name="Type Hidden")
    # Metadata
    class Meta:
        db_table = "source_type"
        ordering = ['type_name']
        verbose_name = "Source Type"
        verbose_name_plural = "Source Types"
    # Methods
    def __str__(self):
        return self.type_name

# Publications (i.e. SuperJump Magazine)
class Publications(models.Model):
    # Fields
    pub_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this publication", verbose_name="Publication Id")
    pub_name = models.CharField(max_length=256,blank=False,null=False,help_text="The name of the publication i.e SuperJump Magazine", verbose_name="Publication Name") 
    pub_url = models.URLField(blank=False,null=False, help_text="URL of the publication, i.e the top level domain", verbose_name="Publication URL")#convert to ip address
    pub_feedurl = models.URLField(blank=False,null=False,help_text="URL of the feed, i.e rss", verbose_name="Publication Feed URL")
    pub_feedtype = models.ForeignKey(SourceType,on_delete=models.RESTRICT,null=True,help_text="The type of feed it is for automation", verbose_name="Feed Type")
    contentsourcedescription = models.CharField(max_length=2000, blank=False,null=False, help_text="Description of the publication, used in the sources page", verbose_name="Publication Description")#change to bigger text? 
    contentsourcehidden = models.BooleanField(default=False, help_text="A flag to determine whether this item should be hidden from the site", verbose_name="Publication Hidden")
    # Metadata
    class Meta:
        db_table = "publications"
        ordering = ['pub_name']
        verbose_name = "publications"
        verbose_name_plural = "publications"
    # Methods
    def __str__(self):
        return self.pub_name
    
# Content Item (the actual links)
class ContentItem(models.Model):
    # Fields
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this content item", verbose_name='Item Id')
    item_title = models.CharField(max_length=256,blank=False,null=False, help_text="The title of the content item i.e blog title", verbose_name="Item Title") 
    item_url = models.URLField(blank=False,null=False, help_text="URL of the content item i.e the url of the article", verbose_name="Item URL")
    item_datepublished = models.DateField(null=True, blank=True, help_text="The date the item was published at it's source, if possible to attain", verbose_name="Item Date Published")
    item_datecreated = models.DateTimeField(auto_now_add=True,null=True, blank=True, help_text="The date the item was created in the app, set to the time of creation", verbose_name= "Item Date Created")
    item_source = models.ForeignKey(Publications, on_delete=models.RESTRICT, null=False, help_text="The source of the item is the name of where it came from i.e SuperJump", verbose_name="Item Source")
    item_votecount = models.IntegerField(default=0,blank=False,help_text="Counts the items popularity", verbose_name="Item Vote Count")
    item_hidden = models.BooleanField(default=False, help_text="A flag to determine whether this item should be hidden from the site", verbose_name="Item Hidden")
    item_curated = models.BooleanField(default=False, help_text="A flag to determine whether this item should be elevated to the curated section", verbose_name="Item Curated")
    # Metadata
    class Meta:
        db_table = "content_item"
        indexes = []
        ordering = ['-item_datepublished']
        verbose_name = "Item"
        verbose_name_plural = "Items"
        constraints = [models.UniqueConstraint(fields=["item_url"], name='unique_url')]
    # Methods
    def __str__(self):
        return self.item_title

# Content Votes
class Votes(models.Model):
    # Fields 
    vote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this vote", verbose_name="New Vote Id" )
    item_id = models.UUIDField(default=uuid.uuid4, help_text="ID of content item", verbose_name="Item ID")
    session_id = models.CharField(max_length=128,blank=False,null=False,help_text="Session ID of the person making the vote", verbose_name="Session ID")
    vote_date = models.DateField(default=timezone.now,help_text="Date vote occured",verbose_name="Date Voted")
    # Metadata
    class Meta:
        db_table = "votes"
        ordering = ['-vote_date']
        verbose_name = "Votes"
        verbose_name_plural = "Votes"
    # Methods
    def __str__(self):
        return str(self.vote_id)

# Publication Form (form for requests)
class PubRequest(models.Model):
    # Fields
    pubreq_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this new source request", verbose_name="New Source Id" )
    pubreq_url = models.URLField(blank=False,help_text="URL of the website top domain", verbose_name="Source URL")
    pubreq_feed = models.URLField(blank=False,help_text="URL of the websites Feed, i.e RSS", verbose_name="Source Feed URL")
    pubreq_name = models.CharField(blank=False,max_length=256,help_text="Name of the person making contact", verbose_name="Contact Name")
    pubreq_email = models.EmailField(blank=False,help_text="The email of the person making contact", verbose_name="Email Address")
    pubreq_notes = models.CharField(blank=True,null=True,max_length=2000,help_text="Notes about the request", verbose_name="Additional Information")
    pubreq_complete = models.BooleanField(default=False, help_text="A flag to determine whether this request has been handled", verbose_name="Source Request Status")
    pubreq_date = models.DateField(default=timezone.now,help_text="Date request was submitted",verbose_name="Date Submitted")
    # Metadata
    class Meta:
        db_table = "publication_request"
        ordering = ['-pubreq_date']
        verbose_name = "Publication Request"
        verbose_name_plural = "Publication Requests"
    # Methods
    def __str__(self):
        return self.pubreq_name 

# Contact Form (form for comments)
class ContactRequest(models.Model):
    contact_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this new contact request", verbose_name="Contact Id" )
    contact_name = models.CharField(blank=False,max_length=256,help_text="Name of the person making contact", verbose_name="Contact Name")
    contact_email = models.EmailField(blank=False,help_text="The email of the person making contact", verbose_name="Contact Email")
    contact_notes = models.CharField(blank=False,max_length=2000,help_text="Notes about the contact request", verbose_name="Additional Information")
    contact_complete = models.BooleanField(default=False, help_text="A flag to determine whether this request has been handled", verbose_name="Contact Request Status")
    contact_date = models.DateField(default=timezone.now,help_text="Date request was submitted",verbose_name="Date Submitted")
    # Metadata
    class Meta:
        db_table = "contact_request"
        ordering = ['-contact_date']
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"
    # Methods
    def __str__(self):
        return self.contactname 
