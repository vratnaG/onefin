from .models import Collection, Movies
from collections import Counter


def get_collection_dict(user_instance):
    collections = Collection.objects.filter(owner=user_instance)
    fav_genrs = [
        movie.genres for collection in collections for movie in collection.movies.all()]
    collection_list = []
    for collection in collections:
        collection_list.append({
            'title': collection.title,
            'uuid': collection.id,
            'description': collection.description
        })
    response = {"is_success": True,
                "data": {
                    "collections": collection_list,
                    "favourite_genres": favourite_genres(fav_genrs)
                }
                }
    return response


def collection_2_dict(collection):
    movies = []
    for movie in collection.movies.all():
        movies.append({
            "title": movie.title,
            "description": movie.description,
            "genres": movie.genres,
            "uuid": movie.id
        })
    data = {
        "title": collection.title,
        "description": collection.description,
        "movies": movies
    }
    return data


def favourite_genres(fav_genrs):
    geners = {}
    for item in fav_genrs:
        geners_name = item.split(',')
        for each in geners_name:
            if each not in geners:
                geners[each] = 0
            else:
                geners[each] += 1
    k = Counter(geners)
    high = k.most_common(3)
    fav = ','.join(dict(high))
    return fav
