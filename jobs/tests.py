from django.test import TestCase
from django.contrib.auth.models import User
from .models import JobApplication
class ApplicationTests(TestCase):
    def setUp(self):
        self.a=User.objects.create_user('alice',password='test-password-984')
        self.b=User.objects.create_user('bob',password='test-password-983')
        self.job=JobApplication.objects.create(user=self.b,company='Private Company',role='Engineer')
        self.client.force_login(self.a)
    def test_private_data(self):
        self.assertNotContains(self.client.get('/'),'Private Company')
        self.assertEqual(self.client.get(f'/applications/{self.job.pk}/edit/').status_code,404)
        self.assertEqual(self.client.post(f'/applications/{self.job.pk}/delete/').status_code,404)
        self.assertNotIn('Private Company',self.client.get('/export/').content.decode())
    def test_create_and_edit(self):
        data={'company':'Demo','role':'Python Developer','status':'applied','applied_date':'2026-10-07'}
        self.assertEqual(self.client.post('/applications/new/',data).status_code,302)
        j=JobApplication.objects.get(user=self.a)
        data['status']='offer'
        self.client.post(f'/applications/{j.pk}/edit/',data)
        j.refresh_from_db()
        self.assertEqual(j.status,'offer')
        self.assertEqual(self.client.get(f'/applications/{j.pk}/delete/').status_code,200)
        self.assertTrue(JobApplication.objects.filter(pk=j.pk).exists())
        self.client.post(f'/applications/{j.pk}/delete/')
        self.assertFalse(JobApplication.objects.filter(pk=j.pk).exists())
    def test_auth_required(self):
        self.client.logout()
        self.assertEqual(self.client.get('/').status_code,302)
    def test_pages_render(self):
        self.assertEqual(self.client.get('/').status_code,200)
        self.assertEqual(self.client.get('/applications/new/').status_code,200)
        self.client.logout()
        self.assertEqual(self.client.get('/login/').status_code,200)
        self.assertEqual(self.client.get('/signup/').status_code,200)
    def test_csv_formula_escaped(self):
        JobApplication.objects.create(user=self.a,company='=1+1',role='Developer')
        self.assertIn("'=1+1",self.client.get('/export/').content.decode())
