from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Colaborator, ItemToBuy, Calculator,
    Movie, Resource, Account, Comment,
    
)

import json


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID')
    username = serializers.CharField(max_length=32,
                                     required=True)
    
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id', 'username']


class UserReadWriteOnlySerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class UserReadOnlySerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source='is_active')
    # full_name = serializers.CharField(source='get_full_name')
    bio = serializers.CharField(source='userprofile.bio')
    birth_date = serializers.DateField(source='userprofile.birth_date')
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'is_staff', 'is_active']
        fields = ['id', 'username', 'full_name', 'email', 
                  'is_staff', 'active', 'bio', 'birth_date']
        
    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class UserProfileSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source='is_active')
    # full_name = serializers.CharField(source='get_full_name')
    bio = serializers.CharField(source='userprofile.bio')
    birth_date = serializers.DateField(source='userprofile.birth_date')
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'is_staff', 'is_active']
        fields = ['id', 'username', 'full_name', 'email', 
                  'is_staff', 'active', 'bio', 'birth_date']
        
    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    

class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'
        # depth = 1
        


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
        fields = ['id', 'title', 'content']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()
        representation['liked-by'] = [user.username for user in instance.liked_by.all()]
        # representation['key'] = self.context['key']
        return representation

    def to_internal_value(self, data):
        resource_data = data['resource']

        return super().to_internal_value(resource_data)
    

def is_rating(value):
    if value < 1:
        raise serializers.ValidationError('Value cannot be lower than 1.')
    elif value > 10:
        raise serializers.ValidationError('Value cannot be higher than 10.')
    return value


class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(validators=[is_rating])
    
    class Meta:
        model = Movie
        fields = '__all__'
        
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating has to be between 1 and 10.')
        return value
    
    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('worldwide_gross cannot be bigger than us_gross')
        return data
        

class CalculatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculator
        fields = '__all__'
        
    def to_representation(self, instance):
        return instance.serialize()


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborator
        fields = '__all__'
        
    
class ItemToBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemToBuy
        fields = '__all__'
        
        
        

