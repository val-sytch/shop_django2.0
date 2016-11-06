from django import template
from mezzanine.conf import settings
from cartridge.shop.models import Product

register = template.Library()

@register.assignment_tag
def get_post_per_page():
    return settings.SHOP_PER_PAGE_CATEGORY

@register.assignment_tag(takes_context=True)
def get_total_posts(context):
    request = context['request']
    return len(Product.objects.published(for_user=request.user))