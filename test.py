from app import app
from models import db, connect_db, User
import unittest

# some different configuration 
# turn off flask debug toolbar INTERCEPTS_REQUESTS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


class BloglyIntegrationTestCase(unittest.TestCase):
    """Integration tests for Blogly app"""

    def setUp(self):
        """run before every single test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        # make a dummy user for testing
        user = User(first_name='Elie',
                last_name='Schoppick',
                image_url='')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        
    def tearDown(self):
        # delete all the users in the table after each test
        user = User.query.get(self.user_id)
        db.session.delete(user)
        db.session.commit()
        

    def test_show_homepage(self):
        """Make sure the user list appears on homepage"""
        client = app.test_client()

        result = client.get("/", follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Users</h2>', result.data)

    def test_add_new_user(self):
        """Make sure new user is added and redirect to homepage. 
        And it will appear on homepage """
        client = app.test_client()

        result = client.post('/users_new',
                            data={'first-name': 'Joel',
                                    'last-name': 'Burton',
                                    'image-url': ''},
                                    follow_redirects=True)
        
        # print("test_add_new_user", result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Joel Burton', result.data)

    # def test_deleting(self):
    #     id = self.user.id

    # What to test:
    # 