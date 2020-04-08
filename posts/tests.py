from django.test import TestCase, Client
from users.forms import User
from posts.models import Post, Follow
from group.models import Group
import time



class TestYatube(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = User.objects.create_user(username = 'test', email = 'test@test.ru', password = 'test123456')
                self.user2 = User.objects.create_user(username = 'test2', email = 'test2@test.ru', password = '123456test')
                self.user3 = User.objects.create_user(username = 'test3', email = 'test3@test.ru', password = '123456test3')
                self.client.post('/auth/login/', {'username': 'test', 'password': 'test123456'}) 
                self.group = Group.objects.create(title="test_group", slug="testgr")
        
        
        def test_profile(self):
                response = self.client.get('/test/')  
                self.assertEqual(response.status_code, 200)

        def test_post(self):
                self.post = Post.objects.create(text="test_text", author=self.user)
                response = self.client.get('/test/')
                self.assertContains(response, "test_text")


        def test_post_no_auth(self):
               self.client.logout()
               response = self.client.get('/new/')  
               self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        def test_public_post(self):
                post = Post.objects.create(text="Тестовый пост!", author=self.user)
                time.sleep(20) 
                response = self.client.get('/')
                self.assertContains(response, "Тестовый пост!")
                response = self.client.get('/test/')
                self.assertContains(response, "Тестовый пост!")
                response = self.client.get(f'/test/{post.id}/')
                self.assertContains(response, "Тестовый пост!")

        def test_edit_post(self):
                self.client.post('/new/', {'text':"Тестовый пост!"}, follow=True)
                post = Post.objects.get(author=self.user)
                self.client.post(f'/test/{post.id}/edit/', {'text':"Тестовый пост (Редакция №1)!"}, follow=True)
                time.sleep(20) 
                response = self.client.get('/')
                self.assertContains(response, "Тестовый пост (Редакция №1)!")
                response = self.client.get('/test/')
                self.assertContains(response, "Тестовый пост (Редакция №1)!")
                response = self.client.get(f'/test/{post.id}/')
                self.assertContains(response, "Тестовый пост (Редакция №1)!")
                
        def test_error_404(self):
                response = self.client.get('/test/test/152')
                self.assertEqual(response.status_code, 404)
        
        def test_add_img(self):
                with open('media/posts/hq-36-768x432_1.jpg', mode='rb') as fp:
                        self.client.post('/new/', {'text': 'This is text', 'image': fp})
                post = Post.objects.get(text='This is text')       
                response = self.client.get(f"/test/{post.id}/")
                self.assertContains(response, 'img')

        def test_add_img_in_index_post_profile(self):
                with open('media/posts/hq-36-768x432_1.jpg', mode='rb') as fp:
                        self.client.post('/new/', {'text': 'This is text', 'image': fp, "group":f'{self.group.id}'})
                response = self.client.get("/test/")
                time.sleep(20) 
                self.assertContains(response, 'img')
                response = self.client.get("/")
                self.assertContains(response, 'img')
                response = self.client.get("/group/testgr/")
                self.assertContains(response, 'img')
        
        def test_add_another_format(self):
                self.client.post('/new/', {'text':"Тестовый пост!"}, follow=True)
                post = Post.objects.get(text='Тестовый пост!')
                with open('media/posts/Тестовый файл.txt', mode='rb') as fp:
                        self.client.post('/test/{post.id}/edit/', {'text': 'format another', 'image': fp})
                response = self.client.get(f"/test/{post.id}/")
                self.assertNotContains(response, 'txt')
        
        def test_job_cash(self):
                self.client.post('/new/', {'text': 'Job cash'})
                time.sleep(20) 
                response = self.client.get('/')
                self.assertContains(response, 'Job cash')

        def test_auth_user_follow(self):
                Follow.objects.create(user=self.user, author=self.user2)
                self.client.logout()
                self.client.post('/auth/login/', {'username': 'test2', 'password': '123456test'})
                self.client.post('/new/', {'text':"Тестовый пост!"}, follow=True)
                self.client.logout()
                self.client.post('/auth/login/', {'username': 'test', 'password': 'test123456'}) 
                response = self.client.get('/follow/')
                self.assertContains(response, "Тестовый пост!")
                Follow.objects.filter(user=self.user).filter(author=self.user2).delete()
                response = self.client.get('/follow/')
                self.assertNotContains(response, "Тестовый пост!")

        def test_new_post_view_follow(self):
                Follow.objects.create(user=self.user, author=self.user2)
                self.client.logout()
                self.client.post('/auth/login/', {'username': 'test2', 'password': '123456test'})
                self.client.post('/new/', {'text':"Тестовый пост!"}, follow=True)
                self.client.logout()
                self.client.post('/auth/login/', {'username': 'test', 'password': 'test123456'}) 
                response = self.client.get('/follow/')
                self.assertContains(response, "Тестовый пост!")
                self.client.logout()
                self.client.post('/auth/login/', {'username': 'test3', 'password': '123456test3'})
                response = self.client.get('/follow/')
                self.assertNotContains(response, "Тестовый пост!")

        def test_add_comment(self):
                self.client.post('/new/', {'text':"test_add_comment"}, follow=True)
                post = Post.objects.get(text='test_add_comment')
                self.client.post(f'/test/{post.id}/comment/', {'text':"comment_text"}, follow=True)
                response = self.client.get(f'/test/{post.id}/')
                self.assertContains(response, 'comment_text')
                self.client.logout()
                self.client.post(f'/test/{post.id}/comment/', {'text':"super new comment_text"}, follow=True)
                response = self.client.get(f'/test/{post.id}/')
                self.assertNotContains(response, 'super new comment_text')
                

              



                


                        
        

                              


        


                