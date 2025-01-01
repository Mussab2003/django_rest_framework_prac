from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['GET', 'POST', 'PUT','PATCH'])
def index(request):
    courses = {
        'course_name' : 'Python',
        'frameworks' : ['django', 'flask', 'fast api'],
    }
    if request.method == 'GET':
        params = request.GET.get('search')
        print(params)
        print('You have hit a get reuqest')
    elif request.method == 'POST':
        body = request.data
        print(body)
        print('You have hit a post request')
    elif request.method == 'PUT':
        print('You have hit a put request')
    elif request.method == 'PATCH':
        print('You have hit a patch request')
    else:
        print('ERROR Incorrent Request')
    return Response(courses)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def people(request):
    if request.method == "GET":
        objs = Person.objects.all()
        serializer =  PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        print(data)
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        data = request.data
        obj = Person.objects.get(id = data['id']).delete()
        return Response('Person deleted successfully')

@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response('User created successfully')
    else:
        return Response(serializer.errors)
    

#class based api views
class Student(APIView):
    def get(self, request):
        return Response('GET request called')
    
    def post(self, request):
        return Response('POST request called')
    
    def delete(
        self, request):
        return Response('DELETE request called')
    


class register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response('User created successfully', status=status.HTTP_201_CREATED)
        
class login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'error' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        token, _ = Token.objects.get_or_create(user = user)
        