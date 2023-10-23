from post import Post

class Blog:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author
        self.posts = []

    def __repr__(self) -> str:
        return f'{self.title} by {self.author} ({len(self.posts)} posts)'
    
    def create_post(self, title: str, content: str) -> None:
        p = Post(title, content)
        self.posts.append(p)

    def json(self):
        return {
            "title": self.title,
            "author": self.author,
            "posts": [p.json() for p in self.posts]
        }