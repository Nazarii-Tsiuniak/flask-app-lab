import unittest
from app import create_app, db
from app.posts.models import Post
from datetime import datetime

class PostsTestCase(unittest.TestCase):
 def setUp(self):
    self.app = create_app("testing")
    self.app.config['WTF_CSRF_ENABLED'] = False
    self.client = self.app.test_client()

    # Тепер імпортуємо і реєструємо блюпринт
    from app.posts import post_bp
    self.app.register_blueprint(post_bp, url_prefix="/posts")

    with self.app.app_context():
        db.create_all()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_posts(self):
        # створюємо тестовий пост
        with self.app.app_context():
            post = Post(
                title="Test Post",
                content="Some content",
                posted=datetime.utcnow(),
                category="test",
                is_active=True,
                author="Tester"
            )
            db.session.add(post)
            db.session.commit()

        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Post", response.data)

    def test_create_post(self):
        response = self.client.post("/posts/create", data={
            "title": "New Post",
            "content": "Some content",
            "category": "news",
            "enabled": True,
            "publish_date": "2025-11-15"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"New Post", response.data)

    def test_post_detail(self):
        with self.app.app_context():
            post = Post(
                title="Detail Post",
                content="Detail content",
                posted=datetime.utcnow(),
                category="info",
                is_active=True,
                author="Tester"
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.get(f"/posts/{post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail Post", response.data)

    def test_edit_post(self):
        with self.app.app_context():
            post = Post(
                title="Edit Post",
                content="Old content",
                posted=datetime.utcnow(),
                category="edit",
                is_active=True,
                author="Tester"
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(f"/posts/{post_id}/update", data={
            "title": "Edited Post",
            "content": "Updated content",
            "category": "edit",
            "enabled": True,
            "publish_date": "2025-11-16"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edited Post", response.data)

    def test_delete_post(self):
        with self.app.app_context():
            post = Post(
                title="Delete Post",
                content="Delete content",
                posted=datetime.utcnow(),
                category="delete",
                is_active=True,
                author="Tester"
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(f"/posts/{post_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Delete Post", response.data)

if __name__ == "__main__":
    unittest.main()
