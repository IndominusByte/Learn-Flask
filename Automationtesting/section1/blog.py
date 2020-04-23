from typing import Dict,Union,List

class Blog:
    def __init__(self,title: str, author: str):
        self.title = title
        self.author = author
        self.posts = []

    def __repr__(self):
        return f"{self.title} by {self.author} Author ({len(self.posts)} post{'s' if len(self.posts) > 1 or len(self.posts) == 0 else ''})"

    def create_post(self,title: str,content: str) -> None:
        post = {'title':title,'content':content}
        self.posts.append(post)

    def json(self) -> Dict[str,Union[str,List]]:
        ret = {
            'title':self.title,
            'author':self.author,
            'posts':self.posts
        }
        return ret
