import re
import urllib2
import requests
from lxml import html
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import File

from cakes.models import Cake, Category


base_url = 'http://www.justbake.in'


def handle_upload_url_file(url):
    # taken from http://stackoverflow.com/a/16177921/1240938
    img_temp = NamedTemporaryFile()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1')]
    img_temp.write(opener.open(url).read())
    img_temp.flush()
    return img_temp


def scrap_categories(url='http://www.justbake.in/bangalore'):
    """parse home page and return dictionary of category name and url"""

    # download home page
    r = requests.get(url)

    # convert downloaded html into lxml tree
    tree = html.fromstring(r.text)

    # fetch all categories
    catgeory_parent_div = tree.xpath('//div[@class="menu container-fluid"]/div/div')[0]

    cat_dict = {} # {'category name': '/href/of/category'}

    for div in catgeory_parent_div.getchildren():
        cat_href = div.xpath('.//a/@href')[0]
        name = div.xpath('.//a/@title')[0]
        print name, cat_href
        cat_dict[name] = base_url + cat_href

    print(cat_dict)
    return cat_dict


def scrap_category_page(category_url):
    """parse category page and scrap items and returns list of products"""

    # download category page
    r = requests.get(category_url)

    tree = html.fromstring(r.text)

    items_div = tree.xpath('//div[@class="col-lg-4 prodcol hidden-xs hidden-sm hidden-md"]')
    products = []
    for item in items_div:
        title = item.xpath('./div[@class="pimg"]/a/@title')[0]
        image_url = base_url + item.xpath('./div[@class="pimg"]/a/img/@src')[0].replace('../', '/')
        price = item.xpath('.//div[@class="green1"]')[0].text.replace('MRP: Rs.', '').strip()
        products.append({
                'title': title,
                'image': image_url,
                'price': price
            })
    return products


def save_products(category_name, cakes):
    category, created = Category.objects.get_or_create(name=category_name)
    for item in cakes:
        cake, created = Cake.objects.get_or_create(title=item['title'], price=item['price'])
        image_url = item['image']
        image_name = image_url.split('/')[-1]
        cake.image.save(image_name, File(handle_upload_url_file(image_url)))
        cake.save()
        category.cakes.add(cake)
        print cake


def fetch_all_cakes():
    # fetch all categories
    categories = scrap_categories()
    for name, url in categories.items():
        print(name, url)
        # fetch all cakes of single category
        cakes = scrap_category_page(url)

        # save to database
        save_products(name, cakes)
