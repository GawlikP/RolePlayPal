from rest_framework import serializers
from .models import Profile 
from django.contrib.auth.models import User 

class ProfileDetailSerializer(serializers.ModelSerializer):
    
    user_username = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = Profile
        read_only_fields = ('id' ,'user_username')
        fields = ['id','user','user_username','created','edited','description','note','preffered_role']

