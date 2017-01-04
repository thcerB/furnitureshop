from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from portfolio.models import Category, Product
from portfolio.forms import CategoryForm, ProductForm, UserForm, UserProfileForm
from datetime import datetime
# Create your views here.

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 5:
        visits = visits + 1

        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val



def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    product_list = Product.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'products' : product_list}
    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']
    response = render(request, 'portfolio/index.html', context_dict)


    return response

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    print(request.method)
    print(request.user)
    return render(request, 'portfolio/about.html', {})


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category=Category.objects.get(slug=category_name_slug)
        products=Product.objects.filter(category=category).order_by('-views')

        context_dict['products']= products
        context_dict['category']= category

    except Category.DoesNotExist:
        context_dict['products']= None
        context_dict['category']= None

    return render(request, 'portfolio/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'portfolio/add_category.html', {'form': form})

@login_required
def add_product(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            if category:
                product = form.save(commit=False)
                product.category = category
                product.views=0
                product.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'portfolio/add_product.html', context_dict)



@login_required
def restricted(request):
    return render(request, 'portfolio/restricted.html',{})


def track_url(request):
    product_id=None
    url='/portfolio/'
    if request.method =='GET':
        if 'product_id' in request.GET:
            product_id = request.GET['product_id']
    if product_id:
            try:
                product=Product.objects.get(id=product_id)
                product.views = product.views + 1
                product.save()
                return redirect(product.url)
            except:
                return HttpResponse("Product id {0} not found".format(product_id))
    print("No product_id in get string")
    return redirect(reverse('index'))

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat=Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list=[]
    if starts_with:
        cat_list=Category.objects.filter(name__istartswith=starts_with)

    if max_results>0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with=''

    if request.method=='GET':
        starts_with=request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)

    return render(request, 'portfolio/cats.html', {'cats':cat_list})
