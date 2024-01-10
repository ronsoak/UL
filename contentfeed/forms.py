from django.forms import ModelForm, Textarea
from contentfeed.models import PubRequest, ContactRequest, ContentItem
from django.utils.translation import gettext_lazy as _

class NewSourceForm(ModelForm):
    class Meta:
        model = PubRequest
        fields = ["pubreq_url","pubreq_feed","pubreq_name","pubreq_email","pubreq_notes"]
        labels = {
            "pubreq_url": _("Website URL"),
            "pubreq_feed": _("Feed URL"),
            "pubreq_name": _("Your Name"),
            "pubreq_email": _("Your Email"),
            "pubreq_notes": _("Notes")
        }
        help_texts = {
            "pubreq_url": _("The address of your website, please include https"),
            "pubreq_feed": _("The address of the feed i.e yoursite.com/rss, please include https"),
            "pubreq_name": _("Please write how you want me to address you"),
            "pubreq_email": _("I'll contact you via this address"),
            "pubreq_notes": _("Please include any additional information about your request.")
        }
        widgets = {
            "pubreq_notes": Textarea()
        }
class NewContactForm(ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["contact_name","contact_email","contact_notes"]
        labels = {
            "contact_name": _("Your Name"),
            "contact_email": _("Your Email"),
            "contact_notes": _("Your Message"),
        }
        help_texts = {
            "contact_name": _(""),
            "contact_email": _(""),
            "contact_notes": _("")
        }
        widgets = {
            "contact_notes": Textarea()
        }