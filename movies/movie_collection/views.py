from .serializers import UserRegsiterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from requests.auth import HTTPBasicAuth
from .constant import USERNAME, PASSWORD, URL, RURL
from .models import Collection, Movies
from .model_dict import get_collection_dict, collection_2_dict
from .movie_collection import movie_add, movie_update


class UserRegsiterView(CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserRegsiterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'access_token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


@api_view(['GET'])
def movies_list(request):
    page = request.GET.get('page', None)
    url = URL
    if page:
        url = URL+'?page='+page
    response = requests.get(url,
                            auth=HTTPBasicAuth(USERNAME, PASSWORD))
    result = response.json()
    if 'next' in result and result['next']:
        print(result['next'].replace(URL, RURL))
        result['next'] = result['next'].replace(URL, RURL)
    if 'previous' in result and result['previous']:
        result['previous'] = result['previous'].replace(URL, RURL)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        response = get_collection_dict(request.user)
        return Response(response, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        owner = request.user
        title = request.data.get('title')
        description = request.data.get('description')
        movies = request.data.get('movies')
        collection_obj = Collection.objects.create(
            title=title, description=description, owner=owner)
        collection_id = movie_add(collection_obj, movies)
        response = {
            'collection_uuid': collection_id
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, uuid):
    try:
        collection = Collection.objects.get(pk=uuid)
    except Collection.DoesNotExist:
        return Response("not found collection", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        response = collection_2_dict(collection)
        return Response(response, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        response = movie_update(collection, request)
        return Response(response, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        collection.delete()
        return Response("delted sucessfully", status=status.HTTP_200_OK)
