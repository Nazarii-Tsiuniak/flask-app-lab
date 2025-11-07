import unittest
from app import create_app, db
from app.posts.models import Post
from datetime import datetime

class PostsTestCase(unittest.TestCase):

    def setUp(self):
        # Тестовий додаток
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        response = self.client.post('/posts/create', data={
            'title': 'Test Post',
            'content': 'This is a test post',
            'category': 'publication',
            'publish_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'enabled': True
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_list_posts(self):
        # створимо пост напряму
        Post.create(title='List Post', content='Content', category='other')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'List Post', response.data)

    def test_post_detail(self):
        post = Post.create(title='Detail Post', content='Content', category='publication')
        response = self.client.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Post', response.data)

    def test_edit_post(self):
        post = Post.create(title='Old Title', content='Old content')
        response = self.client.post(f'/posts/{post.id}/update', data={
            'title': 'New Title',
            'content': 'Updated content',
            'category': 'other',
            'publish_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'enabled': True
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Title', response.data)

    def test_delete_post(self):
        post = Post.create(title='Delete Post', content='To delete')
        response = self.client.post(f'/posts/{post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # перевірка, що пост видалений
        self.assertIsNone(Post.query.get(post.id))

if __name__ == '__main__':
    unittest.main()
