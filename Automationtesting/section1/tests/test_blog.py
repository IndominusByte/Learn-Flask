import os,sys, unittest

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../')
sys.path.append(basedir)

from blog import Blog

class BlogTest(unittest.TestCase):
    def test_blog_create(self):
        blog = Blog('title','author')
        self.assertEqual('title',blog.title)
        self.assertEqual('author',blog.author)
        self.assertListEqual([],blog.posts)

    def test_create_post(self):
        blog = Blog('title','author')
        blog.create_post('test1','content1')
        self.assertListEqual([{'title':'test1','content':'content1'}],blog.posts)

    def test_repr(self):
        blog = Blog('Test','Test')
        b2 = Blog('test2','author2')
        self.assertEqual(blog.__repr__(),'Test by Test Author (0 posts)')
        self.assertEqual(b2.__repr__(),'test2 by author2 Author (0 posts)')

    def test_repr_multiple_post(self):
        blog = Blog('Test','Test')
        blog.posts = ['test']
        self.assertEqual(blog.__repr__(),'Test by Test Author (1 post)')
        blog.posts = ['test','test']
        self.assertEqual(blog.__repr__(),'Test by Test Author (2 posts)')

    def test_json(self):
        blog = Blog('title','author')
        self.assertDictEqual({'title':'title','author':'author','posts':[]},blog.json())

if __name__ == '__main__':
    unittest.main()
