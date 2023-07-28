from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import (
    authenticate, login as login_user, logout as logout_user
)
from django.contrib.auth.decorators import (
    login_required
)
from django.views.decorators.http import (
    require_POST
)
from rest_framework.decorators import api_view
from .models import (
    Colaborator, ItemToBuy, Calculator,
    Distance, Color,
)
from .forms import (
    CollaboratorForm, BinarySearchForm,
    LoginForm, ItemToBuyForm, UserForm,
    FileInformation
)
from .binary_search import binarySearch, get_random, sort_values

import json
from dataclasses import dataclass
from geopy.geocoders import Nominatim
from math import asin, cos, radians, sin, sqrt

from .generals import (
    Fraction,
)



def calculate_fractions(request, nume1, deno1, nume2, deno2, operator):
    fr1 = Fraction(int(nume1), int(deno1))
    fr2 = Fraction(int(nume2), int(deno2))
    result = 'None'

    if operator == '+':
        result = fr1 + fr2
    if operator == '-':
        result = fr1 - fr2
    if operator == 'x':
        result = fr1 * fr2
    if operator == ':':
        result = fr1 / fr2

    return JsonResponse({
        'result': str(result)
    })


def fraction_calculator(request):

    return render(request,
                  'portal/fraction_calculator.html',
                  {'colors': ''})


def file_information(request):
    if request.method == 'POST':
        form = FileInformation(request.POST,
                               request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
    else:
        form = FileInformation()
        
    return render(request,
                  'portal/file_information.html',
                  {'form': form})


def total_colors(request):
    total = Color.objects.count()
    
    return JsonResponse({
        'total_colors': total    
    })

def color_search(request, limit=20):
    colors = Color.objects.all()[limit:limit+10]
    
    return render(request,
                  'portal/color_search.html',
                  {'colors': colors})


def check_value(val):
    if val >= 0 and val <= 255:
        return val
    raise TypeError('Color value must be between 0 and 255 incluvise')

class myColor():
    def __init__(self):
        self.red = 50
        self.green = 75
        self.blue = 100
        
    # TODO: use getattr do dynamically return a value
    def __getattr__(self, attr):
        if attr == "rbgcolor":
            return (self.red, self.green, self.blue)
        elif attr == 'hexcolor':
            return "#{0:02x}{1:02x}{2:02x}".format(
                self.red, self.green, self.blue    
            )
        else:
            raise AttributeError(f'myColor class does not have {attr!r} attribute')
    
    # TODO: use setattr do dynamically return a value
    def __setattr__(self, attr, val):
        if attr == "rgbcolor":
            self.red = check_value(val[0])
            self.green = check_value(val[1])
            self.blue = check_value(val[2])
        else:
            super().__setattr__(attr, val)
    
    # TODO: use dir to list the available properties
    def __dir__(self):
        return ("red", "green", "blue", "rbgcolor", "hexcolor")



@api_view(['POST'])
def color_picker_api(request):
    data = request.data
    red = int(data['red'])
    green = int(data['green'])
    blue = int(data['blue'])
    
    color = Color.objects.filter(
        red=red, green=green, blue=blue)
    if color.exists():
        print(f'{str(color)} already exists')
    else:
        color = Color.objects.create(
            red=red, green=green, blue=blue)
        color.save()
        print('Creating new color.')
    
    cls1 = myColor()
    cls1.rgbcolor = (red, green, blue)
    
    
    return JsonResponse({
        'color': cls1.hexcolor    
    })

def color_picker(request):
    
    return render(request,
                  'portal/color_picker.html')



@dataclass
class Position:
    name: str
    lon: float = 0.0
    lat: float = 0.0

    def distance_to(self, other):
        r = 6371  # Earth radius in kilometers
        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2)**2
             + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)
        return 2 * r * asin(sqrt(h))
    
    
geolocator = Nominatim(user_agent="MyApp")
# loc = geolocator.geocode("Maputo")


@api_view(['POST'])
def distance_between_two_places_api(request):
    data = request.data
    city_1_lat = float(data['lat1'])
    city_1_lon = float(data['lon1'])
    city_2_lat = float(data['lat2'])
    city_2_lon = float(data['lon2'])
    
    d = Distance.objects.filter(
        latitude1=city_1_lat,
        longetude1=city_1_lon,
        latitude2=city_2_lat,
        longetude2=city_2_lon
    )
    if d.exists():
        pass
    else:
        d = Distance.objects.create(
            latitude1=city_1_lat,
            longetude1=city_1_lon,
            latitude2=city_2_lat,
            longetude2=city_2_lon
        )
        d.save()
    
    city_1 = Position('Maputo', city_1_lat, city_1_lon)
    city_2 = Position('New York', city_2_lat, city_2_lon)
    distance = city_1.distance_to(city_2)
    distance = round(distance, 4)
    
    print(f'Distance between ({city_1_lat}ºN, {city_1_lon}ºE) and ({city_2_lat}ºN {city_2_lon}ºE) = {distance} Km')
    
    return JsonResponse({
        'distance': distance    
    })
    

def distance_between_two_places(request):
    return render(request,
                  'portal/distance_between_two_places.html')


def selenium_practie(request):
    return render(request,
                  'portal/selenium_practice.html')


def calculate(request, first_number, second_number, operator):
    obj = Calculator.objects.create(
        first_number=first_number,
        second_number=second_number,
        operator=operator
    )
    obj.save()
    return JsonResponse({
        'result': 'Calculation created!'
    })


def all_items_order_by(request, colname):
    items = ItemToBuy.objects.filter(price__gt=0)
    items = items.order_by(colname)
    data = []
    for item in items:
        data.append(item.serialize())
        
    return JsonResponse({
        'items': data    
    })


# @login_required(login_url='/accounts/login/')
@api_view(['POST'])
def update_item(request):
    data = request.data['data']
    pk = data['id']
    item = ItemToBuy.objects.filter(pk=pk)
    if item.exists():
        item = item.first()
        item.item_name = data['item_name']
        item.price = data['price']
        item.quantity = data['quantity']
        item.category = data['category']
        item.priority = data['priority']
        item.save()
    
    return JsonResponse({
        'data': data    
    })


def get_item_by_pk(request, pk):
    item = ItemToBuy.objects.filter(pk=pk)

    if item.exists():
        item = item.first().serialize()
    else:
        item = []
        
    return JsonResponse({
        'item': item
    })




def delete_item(request, pk):
    item = ItemToBuy.objects.filter(pk=pk)
    # deleted = False
    if item.exists():
        item = item.first()
        item.delete()
        # deleted = True
        
    return redirect("/things_to_by/")
        
    # return JsonResponse({
    #     'deleted': deleted
    # })

def get_all_items(request):
    items = ItemToBuy.objects.filter(price__gt=0)
    data = []
    for item in items:
        data.append(item.serialize())
        
    return JsonResponse({
        'items': data
    })


def get_unique(arr):
    new_arr = []
    for row in arr:
        if row not in new_arr:
            new_arr.append(row)
    return new_arr


# @require_POST
@api_view(['POST'])
def get_categories(request):
    filters = request.data['filters']
    data = []            
    
    for filter_ in filters:
        category_items = ItemToBuy.objects.filter(
            category=filter_)
        priority_items = ItemToBuy.objects.filter(
            priority=filter_)
        
        if category_items.exists():
            data += category_items
        if priority_items.exists():
            data += priority_items
            
    data = get_unique(data)

        
    items = []
    for item in data:
        items.append(item.serialize())
    
    
    return JsonResponse({
        'data': items    
    })


def all_things_to_buy_by_priority(request, priority):
    items = ItemToBuy.objects.filter(
        priority=priority)
    data = []
    if items.exists():
        for item in items:
            data.append(item.serialize())
    else:
        pass
    
    return JsonResponse({
        'items': data  
    })



def all_things_to_buy_by_category(request, category):
    items = ItemToBuy.objects.filter(
        category=category)
    data = []
    if items.exists():
        for item in items:
            data.append(item.serialize())
    else:
        pass
    
    return JsonResponse({
        'items': data  
    })


def things_to_by_filter(request, category=None):
    items = ItemToBuy.objects.filter(category=category)
    item1 = items[0]
    form = ItemToBuyForm()
        
    return render(request,
                  'portal/things_to_by.html',
                  {'items': items,
                   'form': form,
                   'item1': item1})


@login_required(login_url='/login/')
def things_to_by(request):
    items = ItemToBuy.objects.filter(price__gt=0) # category='cotas')
    items = items.order_by('item_name')
    item1 = items[0]
        
    if request.method == 'POST':
        form = ItemToBuyForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            items = items.order_by('item_name')
        else:
            print(form.errors)
    else:
        form = ItemToBuyForm()

    # items = {}
        
    return render(request,
                  'portal/things_to_by.html',
                  {'items': items,
                   'form': form,
                   'item1': item1})
    


def logout(request):
    logout_user(request)
    return redirect('/login/')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            
            user = authenticate(request, 
                                username=username,
                                password=password)
            if user is not None:
                login_user(request, user)
                return redirect('/things_to_by/')
            
            return redirect('/login/')
    else:
        form = LoginForm()
        
    return render(request,
                  'portal/login.html',
                  {'form': form})


def sort_array(request, arr):
    new_arr = []
    for val in arr:
        try:
            val = int(val)
            new_arr.append(val)
        except:
            pass
        
    new_arr = sort_values(new_arr)
    
    return JsonResponse({'sorted_array': new_arr})


def binary_search(request):
    num = 9
    arr = get_random(num)
    num = list(range(num))
    sorted_arr = []
    
    if request.method == 'POST':
        form = BinarySearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nums = list(data.values())
            sorted_arr = sort_values(nums)
    else:
        form = BinarySearchForm()
    
    return render(request,
                  'portal/binary_search.html',
                  {'arr': arr,
                   'num': num,
                   'form': form,
                   'sorted_arr': sorted_arr})


def collaborator_api(request, first_name):
    collaborators = Colaborator.objects.filter(
        first_name=first_name)
    data = {'collaborator': 'Does not exist!'}
    if collaborators.exists():
        users = []
        for user in collaborators:
            users.append(user.serialize())
        # collaborator = collaborator.first().serialize()
        data = {'collaborator': users}
    
    return JsonResponse(data)


def collaborators_api(request):
    collaborators = Colaborator.objects.all()
    data = []
    for col in collaborators:
        data.append(col.serialize())
    
    return JsonResponse({
        'collaborators': data
    })


def confirm_identity(request, username):
    collaborator = Colaborator.objects.filter(
        username=username    
    )
    username_exists = False
    if collaborator.exists():
        username_exists = True
        
    return JsonResponse({
        'username_exists': username_exists    
    })


def view_all_collaborators(request):
    collaborators = Colaborator.objects.all()
    fields = ['username', 'first_name', 'last_name', 'email',
              'department', 'division', 'job_title']
    return render(request,
                  'portal/all_collaborators.html',
                  {'collaborators': collaborators,
                   'fields': fields})


def search_collaborator(request, username):
    collaborator = Colaborator.objects.filter(
        username=username    
    )
    if collaborator.exists():
        collaborator = collaborator.first()
    else:
        collaborator = None
        
    return render(request,
                  'portal/search-collaborator.html',
                  {'collaborator': collaborator})


def register_employee(request):
    only_form = True
    user_exists = False
    if request.method == 'POST':
        form = CollaboratorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['email'] = data['first_name'].lower() + '.' + data['last_name'].lower() + '@portal.co.mz'
            print(f"EMAIL = {data['email']}")
            title = 'Confirmation'
            try:
                collaborator = Colaborator.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    department=data['department'],
                    division=data['division'],
                    job_title=data['job_title']
                )
                collaborator.save()
                is_created = True
                only_form = False
            except Exception:
                collaborator = None
                is_created = False
                user_exists = True
                return render(request,
                              'portal/register_employee.html',
                              {'form': form,
                               'is_created': is_created,
                               'user_exists': user_exists,
                               'collaborator': collaborator,
                               'only_form': only_form,
                               'title': title})
                
            return render(request,
                          'portal/register_employee.html',
                          {'form': form,
                           'is_created': is_created,
                           'user_exists': user_exists,
                           'collaborator': collaborator,
                           'only_form': only_form,
                           'title': title})
            
    else:
        form = CollaboratorForm()
        title = 'Registration'
    
    return render(request,
                  'portal/register_employee.html',
                  {'form': form,
                   'only_form': only_form,
                   'title': title})

