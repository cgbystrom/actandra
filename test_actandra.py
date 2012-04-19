import unittest
import actandra
from utils import truncate

a = actandra

class TestActandra(unittest.TestCase):

    def setUp(self):
        truncate()

    def test_subscribe(self):
        self.assertEquals([], actandra.get_subscribers('elvis'))
        actandra.subscribe('elvis', 'frank')
        actandra.subscribe('elvis', 'julia')
        self.assertEquals(['frank', 'julia'], actandra.get_subscribers('elvis'))

    def test_unsubscribe(self):
        actandra.subscribe('elvis', 'frank')
        actandra.subscribe('elvis', 'julia')
        actandra.unsubscribe('elvis', 'frank')
        self.assertEquals(['julia'], actandra.get_subscribers('elvis'))

    def test_add_activity_to_stream(self):
        msg = 'Ranked up to level 29'
        a.subscribe('frank', 'elvis')
        a.subscribe('frank', 'julia')
        a.add_activity_to_stream('frank', 'random_user', msg)
        elvis_stream = a.get_activity_stream('elvis', 10)
        julia_stream = a.get_activity_stream('julia', 10)
        self.assertEquals(elvis_stream, julia_stream)
        activity = elvis_stream.values()[0]
        self.assertEquals(activity['actor'], 'random_user')
        self.assertEquals(activity['message'], msg)

    def test_add_comment(self):
        aid = a.add_activity_to_stream('frank', 'random_user', 'Ranked up to level 29')
        self.assertEquals(a.get_activity(aid)['numComments'], 0)
        a.add_comment(aid, 'another_random_user', 'Hey, nice level-up!')
        a.add_comment(aid, 'julia', 'I agree.')
        self.assertEquals(a.get_activity(aid)['numComments'], 2)
        comments = a.get_commments(aid, 10)
        self.assertEquals(len(comments), 2)
        self.assertEquals(comments[0]['actor'], 'julia')
        self.assertEquals(comments[0]['comment'], 'I agree.')
        self.assertEquals(comments[1]['actor'], 'another_random_user')
        self.assertEquals(comments[1]['comment'], 'Hey, nice level-up!')

    def test_add_like(self):
        aid = a.add_activity_to_stream('frank', 'random_user', 'Ranked up to level 29')
        self.assertEquals(a.get_activity(aid)['numLikes'], 0)

        a.add_like(aid, 'elvis')
        a.add_like(aid, 'julia')
        self.assertEquals(a.get_activity(aid)['numLikes'], 2)
        likes = a.get_likes(aid)
        self.assertEquals(likes, ['elvis', 'julia'])

        a.remove_like(aid, 'julia')
        self.assertEquals(a.get_activity(aid)['numLikes'], 1)

if __name__ == '__main__':
    unittest.main()

