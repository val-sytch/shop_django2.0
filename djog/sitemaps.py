from __future__ import unicode_literals

from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from mezzanine.core.models import Displayable
from mezzanine.utils.sites import current_site_id

class DisplayableSitemap(Sitemap):
    """
    Sitemap class for Django's sitemaps framework that returns
    all published items for models that subclass ``Displayable``.
    """

    def items(self):
        """
        Return all published items for models that subclass
        ``Displayable``, excluding those that point to external sites.
        """
        return list(Displayable.objects.url_map(in_sitemap=True).values())

    def get_urls(self, **kwargs):
        """
        Ensure the correct host by injecting the current site.
        """
        kwargs["site"] = Site.objects.get(id=current_site_id())
        return super(DisplayableSitemap, self).get_urls(**kwargs)
