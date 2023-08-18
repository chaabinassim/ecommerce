from django.shortcuts import render,redirect,get_object_or_404
from products.models import *
from django.core.cache import cache
from django.db.models import Case, When, BooleanField
from customization.models import Section

def home(request):
    
    try:
        hero_section = Section.objects.get(name="Hero")
    except Section.DoesNotExist:
        # Handle the case where the section with the given name doesn't exist
        hero_section = None

    try:
        collections_section = Section.objects.get(name="collections")
    except Section.DoesNotExist:
        collections_section = None

    try:
        products_section = Section.objects.get(name="products")
    except Section.DoesNotExist:
        products_section = None

    try:
        features_section = Section.objects.get(name="features")
    except Section.DoesNotExist:
        features_section = None
    
    

    featured_products = Product.objects.annotate(
        featured_rank=Case(
            When(is_featured=True, then=1),
            default=0,
            output_field=BooleanField()
        )
    ).filter(featured_rank=True)[:4]

    
    max_products = 4
    context = {
       
        'featured_products': featured_products,
        'hero_section':hero_section,
        'collections_section':collections_section,
        'products_section':products_section,
        'features_section':features_section,
        'max_products'     :max_products,
        
        }
    
    return render(request,'home.html',context)

def collections(request):

    collections = Collection.objects.all()
    context = {
        'collections' :collections,
    }
    return render(request,'collections.html',context)


def collection_detail(request,collection_slug):

    collection = get_object_or_404(Collection, slug=collection_slug)
    related_products = collection.products.all()  

    context = {
        'collection': collection,
        'related_products': related_products,
    }
    return render(request, 'collection_detail.html', context)