from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserTestCase(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
    
    def test_users_list(self):
        """Тест списка пользователей"""
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)
    
def test_user_create(self):
    """Тест создания пользователя"""
    response = self.client.get(reverse('user_create'))
    self.assertEqual(response.status_code, 200)
    
    users_count = User.objects.count()
    response = self.client.post(reverse('user_create'), {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'password1': 'testpass123!@#',
        'password2': 'testpass123!@#',
    })
    
    # Если форма невалидна, выводим ошибки
    if response.status_code != 302:
        print("Form errors:", response.context['form'].errors if 'form' in response.context else 'No form')
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(User.objects.count(), users_count + 1)
    self.assertTrue(User.objects.filter(username='testuser').exists())
    
def test_user_update_self(self):
    """Тест обновления своего профиля"""
    self.client.force_login(self.user1)
    response = self.client.get(reverse('user_update', args=[self.user1.pk]))
    self.assertEqual(response.status_code, 200)
    
    # Получаем текущие данные пользователя
    old_username = self.user1.username
    
    response = self.client.post(reverse('user_update', args=[self.user1.pk]), {
        'first_name': 'Updated',
        'last_name': 'Name',
        'username': old_username,  # Имя пользователя должно остаться
        'password1': 'newpass123!@#',
        'password2': 'newpass123!@#',
    })
    
    # Если форма невалидна, выводим ошибки для отладки
    if response.status_code != 302:
        print("Form errors:", response.context['form'].errors if 'form' in response.context else 'No form')
    
    self.assertEqual(response.status_code, 302)
    self.user1.refresh_from_db()
    self.assertEqual(self.user1.first_name, 'Updated')
    def test_user_update_another_user(self):
        """Тест попытки обновления чужого профиля"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('user_update', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)
    
    def test_user_delete_self(self):
        """Тест удаления своего профиля"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('user_delete', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 200)
        
        users_count = User.objects.count()
        response = self.client.post(reverse('user_delete', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), users_count - 1)
    
    def test_user_delete_another_user(self):
        """Тест попытки удаления чужого профиля"""
        self.client.force_login(self.user1)
        response = self.client.post(reverse('user_delete', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())
    
    def test_login(self):
        """Тест входа"""
        response = self.client.post(reverse('login'), {
            'username': self.user1.username,
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_logout(self):
        """Тест выхода"""
        self.client.force_login(self.user1)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

from task_manager.models import Status


class StatusTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
    
    def test_statuses_list_not_authenticated(self):
        """Тест: список статусов недоступен без авторизации"""
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
    
    def test_statuses_list_authenticated(self):
        """Тест: список статусов доступен авторизованным"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status1.name)
    
    def test_status_create(self):
        """Тест создания статуса"""
        self.client.force_login(self.user)
        statuses_count = Status.objects.count()
        
        response = self.client.post(reverse('status_create'), {
            'name': 'Новый статус',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), statuses_count + 1)
        self.assertTrue(Status.objects.filter(name='Новый статус').exists())
    
    def test_status_update(self):
        """Тест обновления статуса"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('status_update', args=[self.status1.pk]), {
            'name': 'Обновлённый статус',
        })
        self.assertEqual(response.status_code, 302)
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'Обновлённый статус')
    
    def test_status_delete(self):
        """Тест удаления статуса"""
        self.client.force_login(self.user)
        statuses_count = Status.objects.count()
        
        response = self.client.post(reverse('status_delete', args=[self.status1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), statuses_count - 1)
        self.assertFalse(Status.objects.filter(pk=self.status1.pk).exists())
