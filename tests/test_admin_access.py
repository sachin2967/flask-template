"""Authorization regression tests for the Flask portfolio starter."""

import os
import unittest
from urllib.parse import urlsplit

os.environ.setdefault("SECRET_KEY", "test-only-secret")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from app import app, db  # noqa: E402
from models import Project, User  # noqa: E402


class AdminAuthorizationTests(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY="test-only-secret",
            SQLALCHEMY_DATABASE_URI="sqlite://",
        )
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            member = User(username="member")
            member.set_password("correct-horse")
            admin = User(username="admin", is_admin=True)
            admin.set_password("correct-horse")
            db.session.add_all([member, admin])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username):
        return self.client.post(
            "/login",
            data={"username": username, "password": "correct-horse"},
            follow_redirects=False,
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_registered_member_cannot_open_admin_or_create_project(self):
        login_response = self.login("member")
        self.assertEqual(login_response.status_code, 302)
        self.assertIn(urlsplit(login_response.headers["Location"]).path, {"/", "/index"})

        self.assertEqual(self.client.get("/admin").status_code, 403)
        self.assertEqual(self.client.get("/add_project").status_code, 403)

    def test_registered_member_cannot_edit_or_delete_projects(self):
        with app.app_context():
            project = Project(title="Protected", description="Test project")
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        self.login("member")
        self.assertEqual(
            self.client.get(f"/edit_project/{project_id}").status_code, 403
        )
        self.assertEqual(
            self.client.post(f"/delete_project/{project_id}").status_code, 403
        )

    def test_trusted_cli_command_can_promote_a_user(self):
        runner = app.test_cli_runner()
        result = runner.invoke(args=["grant-admin", "member"])
        self.assertEqual(result.exit_code, 0, result.output)
        with app.app_context():
            member = User.query.filter_by(username="member").one()
            self.assertTrue(member.is_admin)

    def test_admin_can_open_admin_panel(self):
        self.login("admin")
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
