from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
# Create your tests here.
add_collection = {
    "title": "my_collection",
    "description": "Description of the collection",
    "movies": [
        {
            "title": "Shadow of the Blair Witch",
            "description": "In this true-crime documentary, we delve into the murder spree that was the inspiration for Joe Berlinger's \"Book of Shadows: Blair Witch 2\".",
            "genres": "Mystery,Horror",
            "uuid": "bcacfa33-a886-4ecb-a62a-6bbcb9d9509d"
        },
        {
            "title": "House of Horrors",
            "description": "An unsuccessful sculptor saves a madman named \"The Creeper\" from drowning. Seeing an opportunity for revenge, he tricks the psycho into murdering his critics.",
            "genres": "Horror,Mystery,Thriller",
            "uuid": "388c99da-0cba-4ff0-a528-faea153b43c3"
        }
    ]
}
update_collection = {
    "title": "my_collection",
    "description": "Description of the collection",
    "movies": [

        {
            "title": "House of Horrors",
            "description": "An unsuccessful sculptor saves a madman named \"The Creeper\" from drowning. Seeing an opportunity for revenge, he tricks the psycho into murdering his critics.",
            "genres": "Horror,Mystery,Thriller",
            "uuid": "388c99da-0cba-4ff0-a528-faea153b43c3"
        },
        {
            "title": "The Burkittsville 7",
            "description": "A film archivist revisits the story of Rustin Parr, a hermit thought to have murdered seven children while under the possession of the Blair Witch.",
            "genres": "Horror",
            "uuid": "5e904ce8-91b7-42b4-84d9-5b53f4cb8c74"
        }
    ]
}


class MovieCollectionTestCase(TestCase):
    def setUp(self):
        self.username = 'testcase'
        self.password = 'test@123'
        self.c = APIClient()

    def get_access(self):
        response = self.c.post(
            '/register/', {'username': self.username, 'password': self.password})
        self.auth_header = 'Bearer ' + response.json()['access_token']
        self.c.credentials(HTTP_AUTHORIZATION=self.auth_header)

    def test_regsiter(self):
        response = self.c.post(
            '/register/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "access_token")

    def test_movies(self):
        self.get_access()
        response = self.c.get('/movies/')
        self.assertEqual(response.status_code, 200)

    def test_collection(self):
        self.get_access()
        response = self.c.get('/collection/')
        self.assertEqual(response.status_code, 200)

        response = self.c.post('/collection/', add_collection, format='json')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "collection_uuid")

        id = response.json()['collection_uuid']

        response = self.c.get('/collection/'+id)
        self.assertEqual(response.status_code, 200)

        response = self.c.put(
            '/collection/'+id, update_collection, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.c.delete('/collection/'+id)
        self.assertEqual(response.status_code, 200)
