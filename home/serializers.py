from rest_framework import serializers
from .models import Person, Color


#So when our model contains a foreign key and we display the data in the get request so we only see the foreign key id.
#If we want to display all the other properties of that foreign table we can add a depth = 1 property in meta table
#But the issue with depth is that it will show all the fields of the foreign table
#If we want to show only the limited fields then instead of using depth, we can create a serializer of that foreign key table and only include the relevant fields

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PeopleSerializer(serializers.ModelSerializer):
    #if we want to display the selected fields of the foreign key properties
    color = ColorSerializer()
    #We can also create a field here without adding it in the model and in order to display the value of this field we have to create a function get_fieldName
    country = serializers.SerializerMethodField()
    class Meta:
        #displays all the property of the foreign key
        # depth = 1
        model = Person
        #Include all the field name that you need to convert from query set to json and vice versa
        # fields = ['name', 'age']
        
        #If you want to include all the fields
        fields = '__all__'

        #If we want to include all the fields but want to exclue any field then we can use exclude
        # exclude = ['name']

    def get_country(self, obj):
        # return ('India')
        #We can also send the other Model content like this:
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color Name' : color_obj.color_name}

    #For custom validation either we can create a function called validate that will contain validation for all the field
    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError('age cannot be less then 18')
        return data
    
    #We can also create individual validation functions for each argument (but the functions should have a prefix of validate_  and the name of the argument)
    #For Age Validation
    # def validate_age(self, age):
    #     if age < 18:
    #         raise serializers.ValidationError('age cannot be less then 18')
    #     return age
    #For Name Validation
    # def validate_name(self, name):
    #     #---Validation logic---
    #     return name