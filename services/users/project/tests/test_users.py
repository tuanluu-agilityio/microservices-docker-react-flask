import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the User Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tuanluu',
                    'email': 'tuan.luu@asnet.com.vn'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('tuan.luu@asnet.com.vn was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object invalid keys"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'tuan.luu@asnet.com.vn'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if email existing"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tuanluu',
                    'email': 'tuan.luu@asnet.com.vn'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tuanluu',
                    'email': 'tuan.luu@asnet.com.vn'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry, That email already exists.', data['message']
            )
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('tuanluu', 'tuan.luu@asnet.com.vn')

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('tuanluu', data['data']['username'])
            self.assertIn('tuan.luu@asnet.com.vn', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get(f'/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exists."""
        with self.client:
            response = self.client.get(f'/users/9999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('tuanluu', 'tuan.luu@asnet.com.vn')
        add_user('tuanluu1', 'tuan.luu1@asnet.com.vn')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            user = data['data']['users']

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(user), 2)
            self.assertIn('tuanluu', user[0]['username'])
            self.assertIn('tuan.luu@asnet.com.vn', user[0]['email'])
            self.assertIn('tuanluu1', user[1]['username'])
            self.assertIn('tuan.luu1@asnet.com.vn', user[1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """
            Ensure the main route behaves correctly when no users have been
            added to the database.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """
            Ensure the main route behaves correctly when users have been added
            to the database.
        """
        add_user("tuan.luu", "tuan.luu@asnet.com.vn")
        add_user("tuan.luu1", "tuan.luu+1@asnet.com.vn")
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'tuan.luu', response.data)
            self.assertIn(b'tuan.luu1', response.data)

    def test_main_add_user(self):
        """
            Ensure the main route behaves correctly when
            add user to the database.
        """
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username="tuanluu", email="tuan.luu@asnet.com.vn"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'tuanluu', response.data)


if __name__ == "__main__":
    unittest.main()
