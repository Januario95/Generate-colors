from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin

from faker import Faker
import random

from .models import (
    Colaborator, ItemToBuy, Calculator,
    Movie, Resource, UserProfile, Account,
    Comment, Distance, Color,
)

def mask_name(name):
    new_chars = ''
    for char in name:
        if char not in 'aeiou':
            new_chars += '*'
        else:
            new_chars += char
    return new_chars


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json', queryset, stream=response)
    return response

export_as_json.short_description = 'Export as JSON'


@admin.register(Color)
class ColorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'red', 'green', 'blue', 'hexcolor',
                    'rgbcolor', 'color_display', 'created_at', 
                    'updated_at']
    list_per_page = 10
    
    def hexcolor(self, obj):
        return mark_safe(f'<span style="color: {obj.hexcolor()};">{obj.hexcolor()}</span>')
    hexcolor.short_description = 'hexcolor'
    
    def rgbcolor(self, obj):
        return obj.rgbcolor()
    rgbcolor.short_description = 'rgbcolor'
    
    def color_display(self, obj):
        # return mark_safe(f'''
        #       <input type="color" value="{obj.hexcolor()}"
        #       style="border-radius:50%; width:50px; height:50px; border: 3px dashed #ccc;"
        #       />
        # ''')
        return mark_safe(f'''
              <p style="background-color: {obj.hexcolor()}; border-radius:50%; width:5px; height:25px; border: 3px solid #ccc;"></p>
        ''')
    color_display.short_description = 'Color Display'

@admin.register(Distance)
class DistanceAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'latitude1_', 'longetude1_', 'latitude2_',
                    'longetude2_', 'distance']
    
    def latitude1_(self, obj):
        return mark_safe(f'{obj.latitude1}ºN')
    latitude1_.short_description = 'Latitude1'
    
    def longetude1_(self, obj):
        return mark_safe(f'{obj.latitude1}ºE')
    longetude1_.short_description = 'Longetude1'
    
    def latitude2_(self, obj):
        return mark_safe(f'{obj.latitude2}ºN')
    latitude2_.short_description = 'latitude2'
    
    def longetude2_(self, obj):
        return mark_safe(f'{obj.longetude2}ºE')
    longetude2_.short_description = 'longetude2'
    
    def distance(self, obj):
        return mark_safe(f'{obj.distance_to()}Km')
    distance.short_description = 'Distance'


@admin.register(Comment)
class CommentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'author', 'datetime', 'content']

@admin.register(Account)
class AccountAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'username']
    

@admin.register(UserProfile)
class UserProfileAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'user', 'bio', 'birth_date']


@admin.register(Movie)
class MovieAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'title', 'description', 'release_date',
                    'rating', 'us_gross', 'worldwide_gross']
    

@admin.register(Resource)
class ResourceAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'title', 'content']


@admin.register(Calculator)
class CalculatorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'first_number', 'second_number',
                    'operator', 'result', 'created_at',
                    'updated_at']
    
    def result(self, obj):
        return obj.result()
    result.short_description = 'Result'


@admin.register(ItemToBuy)
class ItemToBuyAdmin(ImportExportActionModelAdmin, admin.ModelAdmin,):
    list_display = ['id', 'item_name', 'price', 'quantity',
                    'priority', 'category', 'buy_from', 'urgent', 
                    'created_at', 'updated_at']
    list_editable = ['price', 'priority', 'category', 
                     'urgent', 'buy_from']
    list_filter = ['priority', 'category', 'urgent']
    actions = [export_as_json]
    search_fields = ['item_name',]
    list_per_page = 10

    # def money_source(self, obj):
    #     return obj.buy_from
    # money_source.short_description = 'Source'


@admin.register(Colaborator)
class ColaboratorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'mask_username', 'first_name', 'last_name',
                    # 'mask_firstName_consonant',
                    # 'mask_lastName_consonant',
                    # 'full_name',
                    'formart_email', 
                    # 'email', 
                    'department',
                    'division', 'job_title',
                    'created_at', 'updated_at']
    ordering = ('id',)
    # list_display_links = ['id', 'username']
    # list_editable = ['job_title',]
    
    def mask_firstName_consonant(self, obj):
        first_name = mask_name(obj.first_name)
        return first_name
    mask_firstName_consonant.short_description = 'First Name'
    
    def mask_lastName_consonant(self, obj):
        last_name = mask_name(obj.last_name)
        return last_name
    mask_lastName_consonant.short_description = 'Last Name'
        
    
    def formart_email(self, obj):
        # email = mask_name(obj.first_name) + '.' + mask_name(obj.last_name) + '@portal.co.mz'
        faker = Faker()
        domain = faker.email().split('@')[1]
        email = random.randint(1, 9)*'*' + '.' + random.randint(1, 9)*'*' + '@' + domain
        return mark_safe(f'''
            <a href="mailto:{email}">{email}</a>
        ''')
    formart_email.short_description = 'Email'
    
    def full_name(self, obj):
        faker  = Faker()
        fullname = faker.last_name().upper() + ', ' + faker.first_name()
        return mark_safe(f'<b>{fullname}</b>')
    
    full_name.short_description = 'Full Name'
    
    def mask_username(self, obj):
        username = random.randint(4, 13) * '*'
        return mark_safe(f'<b title={username}>{username}</b>')
    
    mask_username.short_description = 'Username'
    

