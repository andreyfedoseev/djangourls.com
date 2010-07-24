from django import forms
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from feeds.models import Feed
import feedparser


class FeedAdminForm(ModelForm):
    
    error_messages = {
        'invalid_feed_url': _(u"This URL does not point to a valid RSS feed."), 
    } 

    def __init__(self, *args, **kwargs):
        super(FeedAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.url:
            self.fields['url'].widget.attrs['disabled'] = "disabled"
        self.fields['source_url'].widget.attrs['disabled'] = "disabled"
        
    def clean_url(self):
        data = self.cleaned_data['url']
        try:
            Feed.objects.get(url=data)
            raise forms.ValidationError(_("The feed with this URL is registered already."))
        except Feed.DoesNotExist:
            pass

        return data
                    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url:
            try:
                parsed = feedparser.parse(url)
            except:
                self._errors["url"] = ErrorList([self.error_messages['invalid_feed_url']])
                del cleaned_data["url"]
                return cleaned_data
            if not parsed.version:
                self._errors["url"] = ErrorList([self.error_messages['invalid_feed_url']])
                del cleaned_data["url"]
                return cleaned_data

        return cleaned_data
    
    def save(self, commit=True):
        old_url = self.instance.url
        instance = super(FeedAdminForm, self).save(commit)
        parsed = feedparser.parse(instance.url)
        if not instance.title or instance.url != old_url:
            instance.title = parsed.feed.title
        instance.source_url = parsed.feed.link
        if commit:
            instance.save()
        return instance
        
    class Meta:
        model = Feed
        fields = ('url', 'title', 'source_url', 'category',)        
        

                