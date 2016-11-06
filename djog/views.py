from django.http import HttpResponse, JsonResponse
from mezzanine.conf import settings
from cartridge.shop.models import Product, ProductVariation, ProductImage
from django.template.defaultfilters import slugify
from django.core import serializers

def moreDogs(request):
    sort_options = [(slugify(option[0]), option[1]) for option in settings.SHOP_PRODUCT_SORT_OPTIONS]
    sort_by = request.GET.get("sortBy", sort_options[0][1])
    startPaging = int(request.GET.get('startPaging', 0))
    offset = startPaging + settings.SHOP_PER_PAGE_CATEGORY
    products = Product.objects.published(for_user=request.user).order_by(sort_by).distinct()[startPaging:offset]
    data = serializers.serialize("json", products)
    #return HttpResponse()
    return JsonResponse(data, safe=False)