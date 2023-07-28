from django.db import models
from django.utils import timezone
from django.db.models import Aggregate, Sum
from django.contrib.auth.models import User

import json
import random
import string
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt


def all_digits(num):
    for x in num:
        try:
            x = int(x)
        except:
            return False
    return True


class Color(models.Model):
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('id',)
    
    def __str__(self):
        return "({0}, {1}, {2}) - #{0:02x}{1:02x}{2:02x}".format(
            self.red, self.green, self.blue,
            self.red, self.green, self.blue
        )
    
    def hexcolor(self):
        return "#{0:02x}{1:02x}{2:02x}".format(
            self.red, self.green, self.blue    
        )
    
    def rgbcolor(self):
        return "({0}, {1}, {2})".format(
            self.red, self.green, self.blue    
        )

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


class Distance(models.Model):
    latitude1 = models.FloatField()
    longetude1 = models.FloatField()
    latitude2 = models.FloatField()
    longetude2 = models.FloatField()
    
    def __str__(self):
        return f'({self.latitude1}ºN, {self.longetude1}ºE) ({self.latitude2}ºN {self.longetude2}ºE)'
    
    def distance_to(self):
        city_1 = Position('Maputo', self.latitude1, self.longetude1)
        city_2 = Position('New York', self.latitude2, self.longetude2)
        distance = city_1.distance_to(city_2)
        distance = round(distance, 4)
        return distance


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return self.author.username
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        

class Account(models.Model):
    username = models.CharField(max_length=32)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, 
                                on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} profile'


class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(to=User)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'


class Movie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    release_date = models.DateField()
    rating = models.PositiveSmallIntegerField()

    us_gross = models.IntegerField(default=0)
    worldwide_gross = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'



OPERATIONS = {
    "sum": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "div": lambda x, y: x / y,
    "multi": lambda x, y: x * y
}

GET_OPERATOR = {
    "sum": "+", "sub": "-", "div": ":", "multi": "*"
}

class Calculator(models.Model):
    first_number = models.FloatField()
    second_number = models.FloatField()
    operator = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.first_number} {GET_OPERATOR[self.operator]} {self.second_number} = {self.result()}'
    
    def result(self):
        res = OPERATIONS[self.operator](self.first_number, self.second_number)
        return round(res, 2)
        
    class Meta:
        verbose_name = 'Calculation'
        verbose_name_plural = 'Calculations'
        
    def serialize(self):
        data = {
            'id': self.id,
            'item_name': self.first_number,
            'price': self.second_number,
            'quantity': self.operator,
            'result': self.result(),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return data
    

def format_username(username):
    letters = string.ascii_letters
    if (len(username) == 7 and username[0] in list('abc') and 
        all_digits(username[1:])):
        return username
    raise TypeError('Username must start with a letter and remaining characters must be digits')


def generate_digits():
    letter = random.choice(list('abc'))
    digits = ''.join([str(random.randint(1, 9)) for _ in range(6)])
    return letter + digits


class ItemToBuyQuerySet(models.QuerySet):
    def serialize(self):
        return json.dumps(self.model('id', 'item_name', 'price', 'quatity',
                                     'priority', 'category', 'urgent', 
                                     'created_at', 'updated_at'))
    
class ItemToBuyManager(models.Manager):
    def get_queryset(self):
        return ItemToBuyQuerySet(self.model, 
                                 using=self._db)
    # PersonQuerySet(self.model, using=self._db)

class ItemToBuy(models.Model):
    CATEGORY = (
        ('clothes', 'Clothes'),
        ('cotas', 'Cotas'),
        ('debt', 'Debt'),
        ('documents', 'Documents'),
        ('family', 'Family'),
        ('food', 'Food'),
        ('house', 'House'),
        ('hygien', 'Hygien'),
        ('utilities', 'Utilities')
    )
    PRIORITY = (
        ('critical', 'Critical'),
        ('moderate', 'Moderate'),
        ('low', 'Low')
    )
    BUY_FROM = (
        ('side-hustle', 'Side-Hustle'),
        ('salary', 'Salary')
    )
    item_name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20, 
                                choices=CATEGORY,
                                default='hygien')
    priority = models.CharField(max_length=20, 
                                choices=PRIORITY,
                                default='critical')
    urgent = models.BooleanField(default=True)
    buy_from = models.CharField(max_length=20,
                                choices=BUY_FROM,
                                default='cabaz')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ItemToBuyManager()
    
    def __str__(self):
        return f'{self.item_name} - {self.price} MZN - {self.quantity} items'
    
    class Meta:
        ordering = ('item_name',)
        verbose_name = ('Item To Buy')
        verbose_name_plural = ('Items To Buy')
        
    def serialize(self):
        data = {
            'id': self.id,
            'item_name': self.item_name,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category,
            'priority': self.priority,
            'urgent': self.urgent,
            'total_amount': self.total_amount(),
            'credit': self.credit(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data
    
    def total_amount(self):
        total = 0
        for item in ItemToBuy.objects.all():
            total += item.price
        return total
    
    def credit(self):
        return 38400 - self.total_amount()


class ColaboratorQuerySet(models.QuerySet):
    def serialize(self):
        return json.dumps(self.model('id', 'username',
                                     'first_name'))
    
class ColaboratorManager(models.Manager):
    def queryset(self):
        return ColaboratorQuerySet(self, self._db)


class Colaborator(models.Model):        
    DEPTS = (
        ('engineering', 'Engineering'),
        ('cib', 'CIB'),
        ('bcc', 'BCC'),
        ('chnw', 'CHNW')
    )
    username = models.CharField(max_length=50, 
                                unique=True, 
                                blank=True,
                                default=generate_digits)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    email = models.EmailField(blank=True, unique=True)
    department = models.CharField(max_length=20,
                                  choices=DEPTS,
                                  default='engineering')
    # department = models.CharField(max_length=200,
    #                               blank=True,
    #                               null=True)
    division = models.CharField(max_length=200,
                                blank=True,
                                null=True)
    job_title = models.CharField(max_length=200,
                                 blank=True,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    objects = ColaboratorManager()
    
    def __str__(self):
        return f'{self.last_name.upper()} {self.first_name}'
    
    class Meta:
        ordering = ('first_name',)
        
    def serialize(self):
        data = {
            'id': self.id,
            'username':len( self.username) * '*',
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'department': self.division,
            'division': self.division,
            'job_title': self.job_title
        }
        return data
        
        
    
    
        
        
        