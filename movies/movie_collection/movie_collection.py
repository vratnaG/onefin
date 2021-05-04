from .models import Collection, Movies
from .model_dict import collection_2_dict


def movie_add(collection, movies):
    for movie in movies:
        if Movies.objects.filter(id=movie['uuid']).exists():
            instance = Movies.objects.get(id=movie['uuid'])
            if not collection.movies.filter(id=instance.id).exists():
                collection.movies.add(instance)
        else:
            instance = Movies.objects.create(id=movie['uuid'], title=movie['title'],
                                             description=movie['description'], genres=movie['genres'])
            collection.movies.add(instance)
    return collection.id


def movie_update(collection, request):
    title = request.data.get('title')
    description = request.data.get('description')
    movies = request.data.get('movies')
    user_list = list(collection.movies.all())
    new_list = []
    for movie in movies:
        if Movies.objects.filter(id=movie['uuid']).exists():
            instance = Movies.objects.get(id=movie['uuid'])
            new_list.append(instance)
        else:
            instance = Movies.objects.create(id=movie['uuid'], title=movie['title'],
                                             description=movie['description'], genres=movie['genres'])
            new_list.append(instance)
    remove_list = list(set(user_list)-set(new_list))
    add_list = list(set(new_list)-set(user_list))
    for del_movie in remove_list:
        collection.movies.remove(del_movie)
    for add_movie in add_list:
        collection.movies.add(add_movie)
    collection.title = title
    collection.description = description
    collection.save()
    return collection_2_dict(collection)
