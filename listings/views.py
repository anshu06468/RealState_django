from django.shortcuts import render
from .models import Listings
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.
def index(request):
    listings = Listings.objects.order_by("-list_date").filter(is_published=True)

    paginator=Paginator(listings,26)
    page = request.GET.get('page')
    paged_listings= paginator.get_page(page)

    context = {
        "listings":paged_listings
    }
    return render(request, "listings/listings.html", context)

def listing(request,listing_id):
    return render(request, "listings/listing.html")

def search(request):
    return render(request, "listings/search.html")
