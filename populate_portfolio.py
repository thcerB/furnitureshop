import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furnitureshop.settings')

import django
django.setup()

from portfolio.models import Category, Product

def populate():


    meubel_products = [
    {"title": "Stoel", "url":"www.stoel.be"},
    {"title": "Zetel", "url":"www.zetel.be"},
    {"title": "Tafel", "url":"www.tafel.be"}]

    lamp_products = [
    {"title": "Staanlamp", "url":"www.staanlamp.be"},
    {"title": "bureaulamp", "url":"www.bureaulamp.be"},
    {"title": "hanglamp", "url":"www.hanglamp.be"}]

    home_products = [
    {"title": "Wijnrek", "url":"www.wijnrek.be"},
    {"title": "Snijplank", "url":"www.snijplank.be"}]


    cats = {"Meubels" : {"products": meubel_products},
            "Lampen" : {"products": lamp_products},
            "Home" : {"products": home_products}}

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["products"]:
            add_product(c, p["title"], p["url"])

    for c in Category.objects.all():
        for p in Product.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_product(cat, title, url, views=0):
    p = Product.objects.get_or_create(category=cat, title=title)[0]
    p.url= url
    p.views = views
    p.save()
    return p

def add_cat(name, views=1, likes=1):
    c= Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

if __name__ =='__main__':
        print("Starting Portfolio population script...")
        populate()
