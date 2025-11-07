import unittest
from app import create_app, db
from app.posts.models import Post
from datetime import datetime, timezone

class PostsTestCase(unittest.TestCase):
    def setUp(self):
        # Створюємо тестовий додаток
        self.app = create_app("testing")
        self.app.config['WTF_CSRF_ENABLED'] = False  # Вимикаємо CSRF для тестів
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # --- Створення поста ---
    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post("/posts/post/create", data={
                "title": "Test Post",
                "content": "This is a test post",
                "publish_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                "category": "news",
                "enabled": True
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)
            self.assertIn(b"Test Post", response.data)

    # --- Перегляд всіх постів ---
    def test_list_posts(self):
        with self.app.app_context():
            post = Post(title="List Post", content="Content")
            db.session.add(post)
            db.session.commit()

            response = self.client.get("/posts/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"List Post", response.data)

    # --- Перегляд одного поста ---
    def test_post_detail(self):
        with self.app.app_context():
            post = Post(title="Detail Post", content="Detail Content")
            db.session.add(post)
            db.session.commit()

            response = self.client.get(f"/posts/post/{post.id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detail Post", response.data)
            self.assertIn(b"Detail Content", response.data)

    # --- Редагування поста ---
    def test_edit_post(self):
        with self.app.app_context():
            post = Post(title="Old Title", content="Old Content")
            db.session.add(post)
            db.session.commit()

            response = self.client.post(f"/posts/post/{post.id}/update", data={
                "title": "Updated Title",
                "content": "Updated Content",
                "publish_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
                "category": "tech",
                "enabled": True
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post updated successfully", response.data)
            self.assertIn(b"Updated Title", response.data)

    # --- Видалення поста ---
    def test_delete_post(self):
        with self.app.app_context():
            post = Post(title="Delete Me", content="Delete Content")
            db.session.add(post)
            db.session.commit()

            # GET-запит на підтвердження
            get_resp = self.client.get(f"/posts/post/{post.id}/delete")
            self.assertEqual(get_resp.status_code, 200)
            self.assertIn(b"Are you sure", get_resp.data)

            # POST-запит для видалення
            post_resp = self.client.post(f"/posts/post/{post.id}/delete", follow_redirects=True)
            self.assertEqual(post_resp.status_code, 200)
            self.assertIn(b"Post deleted successfully", post_resp.data)

if __name__ == "__main__":
    unittest.main()
