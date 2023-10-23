from unittest import TestCase
from unittest.mock import patch
import app
from blog import Blog
from post import Post

class AppTest(TestCase):
    def setUp(self) -> None:
        b = Blog("Test", "Test Author")
        app.blogs = {b.title: b}


    def test_menu_prints_prompt(self):
        with patch("builtins.input", return_value="q") as mocked_input:
            app.menu()
            mocked_input.assert_called_with(app.MENU_PROMPT)

    def test_menu_shows_print_blogs(self):
        with patch("app.print_blogs") as mocked_print_blogs:
            with patch("builtins.input", return_value="q"):
                app.menu()
                mocked_print_blogs.assert_called_once()

    def test_menu_calls_ask_create_blog(self):
        with patch("app.ask_create_blog") as mocked_ask_create_blog:
            with patch("builtins.input", side_effect=["c", "q"]):
                app.menu()
                mocked_ask_create_blog.assert_called_once()


    def test_menu_calls_print_blogs(self):
        with patch("app.print_blogs") as mocked_print_blogs:
            with patch("builtins.input", side_effect=["l", "q"]):
                app.menu()
                self.assertEqual(mocked_print_blogs.call_count, 2)


    def test_menu_calls_ask_read_blog(self):
        with patch("app.ask_read_blog") as mocked_ask_read_blog:
            with patch("builtins.input", side_effect=["r", "q"]):
                app.menu()
                mocked_ask_read_blog.assert_called_once()


    def test_menu_calls_ask_create_post(self):
        with patch("app.ask_create_post") as mocked_ask_create_post:
            with patch("builtins.input", side_effect=["p", "q"]):
                app.menu()
                mocked_ask_create_post.assert_called_once()


    def test_print_blogs(self):
        with patch("builtins.print") as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with("- Test by Test Author (0 posts)")

    
    def test_ask_create_blog(self):
        test_title, test_author = "Test Title", "Test Author"
        with patch("builtins.input", side_effect=[test_title, test_author]):
            app.ask_create_blog()
            expected = Blog(test_title, test_author).json()

            self.assertEquals(len(app.blogs), 2)
            self.assertDictEqual(app.blogs[test_title].json(), expected)


    def test_ask_read_blog(self):
        with patch("builtins.input", return_value="Test"):
            with patch("app.print_posts") as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_once_with(app.blogs["Test"])

    def test_print_posts(self):
        b = app.blogs["Test"]
        b.create_post("Test Post", "Test Content")

        with patch("app.print_post") as mocked_print_post:
            app.print_posts(b)

            mocked_print_post.assert_called_once_with(b.posts[0])

    def test_print_post(self):
        p = Post("Test Post", "Test Content")
        expected_print = """
--- Test Post ---

Test Content

"""

        with patch("builtins.print") as mocked_print:
            app.print_post(p)

            mocked_print.assert_called_once_with(expected_print)

    def test_ask_create_post(self):
      
        with patch("builtins.input", side_effect=["Test", "Test Post", "Test Content"]):
            with patch("blog.Blog.create_post") as mocked_create_post:
                app.ask_create_post()

                mocked_create_post.assert_called_once_with("Test Post", "Test Content")