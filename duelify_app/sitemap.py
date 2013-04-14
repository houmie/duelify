from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from duelify_app.models import Ring

class Sitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 1
    protocol = 'https'

    def items(self):
        return Ring.objects.order_by('-datetime') 

    def lastmod(self, obj):
        return obj.datetime

    def location(self, obj):
        return reverse('discuss-topic', kwargs={'ring_id':str(obj.id), 'slug':obj.slug})