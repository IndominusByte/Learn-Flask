from basetest import BaseTest, unittest

class HomeTest(BaseTest):
    def test_home(self):
        with self.app() as c:
            res = c.get('/')
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(res.get_json(),{'message':'nice'})

if __name__ == '__main__':
    unittest.main()
