import unittest
from unittest.mock import patch
from data.random_users import RandomUser
from main import app
from data import db_session

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        db_session.global_init("db.sqlite")
        self.app = app.test_client()
        self.app.testing = True

    def test_main_page_get(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    @patch("main.requests.get")
    def test_main_page_post_mocked(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [{
                "gender": "female",
                "name": {"first": "Elizaveta", "last": "Uglova"},
                "phone": "8915-224",
                "email": "edeu03@mail.ru",
                "location": {"city": "Moscow", "country": "Russia"},
                "picture": {"thumbnail": "https://example.com/photo.jpg"}
            }]
        }

        response = self.app.post("/", data={"count": "1"})
        self.assertEqual(response.status_code, 200)

    def test_random_user_page(self):
        response = self.app.get("/random")
        self.assertIn(response.status_code, [200, 404])

    def test_user_detail_page(self):
        db = db_session.create_session()
        user = db.query(RandomUser).first()
        if user:
            response = self.app.get(f"/user/{user.id}")
            self.assertEqual(response.status_code, 200)
        else:
            print("Нет пользователей в базе для /user/<id>")

if __name__ == "__main__":
    unittest.main()
