import os,sys,unittest
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../')
sys.path.append(basedir)

from post import Post

class PostTest(unittest.TestCase):
    def test_create_post(self):
        post = Post('Title','Content')
        self.assertEqual('Title',post.title)
        self.assertEqual('Content',post.content)

    def test_json(self):
        post = Post('title','content')
        expected = {"title":"title","content":"content"}
        self.assertDictEqual(expected,post.json())

if __name__ == '__main__':
    unittest.main()
