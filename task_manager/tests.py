from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.models import Status, Task, Label


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
        
        old_username = self.user1.username
        
        response = self.client.post(reverse('user_update', args=[self.user1.pk]), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': old_username,
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#',
        })
        
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


class TaskTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.task1 = Task.objects.get(pk=1)

    def test_tasks_list_not_authenticated(self):
        """Тест: список задач недоступен без авторизации"""
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 302)

    def test_tasks_list_authenticated(self):
        """Тест: список задач доступен авторизованным"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)

    def test_task_create(self):
        """Тест создания задачи"""
        self.client.force_login(self.user1)
        tasks_count = Task.objects.count()
        status = Status.objects.first()

        response = self.client.post(reverse('task_create'), {
            'name': 'Новая задача',
            'description': 'Описание задачи',
            'status': status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), tasks_count + 1)
        new_task = Task.objects.get(name='Новая задача')
        self.assertEqual(new_task.author, self.user1)

    def test_task_update(self):
        """Тест обновления задачи"""
        self.client.force_login(self.user1)
        status = Status.objects.first()

        response = self.client.post(
            reverse('task_update', args=[self.task1.pk]),
            {
                'name': 'Обновлённая задача',
                'description': 'Новое описание',
                'status': status.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Обновлённая задача')

    def test_task_delete_by_author(self):
        """Тест удаления задачи автором"""
        self.client.force_login(self.user1)
        tasks_count = Task.objects.count()

        response = self.client.post(
            reverse('task_delete', args=[self.task1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), tasks_count - 1)

    def test_task_delete_by_non_author(self):
        """Тест попытки удаления задачи не автором"""
        self.client.force_login(self.user2)
        tasks_count = Task.objects.count()

        response = self.client.post(
            reverse('task_delete', args=[self.task1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), tasks_count)

    def test_task_detail(self):
        """Тест просмотра задачи"""
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse('task_detail', args=[self.task1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)

    def test_task_filter_by_status(self):
        """Тест фильтрации задач по статусу"""
        self.client.force_login(self.user1)
        status = Status.objects.first()
        
        response = self.client.get(
            reverse('tasks_list'),
            {'status': status.pk}
        )
        self.assertEqual(response.status_code, 200)
        for task in response.context['filter'].qs:
            self.assertEqual(task.status, status)

    def test_task_filter_by_executor(self):
        """Тест фильтрации задач по исполнителю"""
        self.client.force_login(self.user1)
        
        response = self.client.get(
            reverse('tasks_list'),
            {'executor': self.user2.pk}
        )
        self.assertEqual(response.status_code, 200)
        for task in response.context['filter'].qs:
            if task.executor:
                self.assertEqual(task.executor, self.user2)

    def test_task_filter_by_label(self):
        """Тест фильтрации задач по метке"""
        self.client.force_login(self.user1)
        label = Label.objects.first()
        
        response = self.client.get(
            reverse('tasks_list'),
            {'labels': label.pk}  # Изменено с 'label' на 'labels'
        )
        self.assertEqual(response.status_code, 200)
        for task in response.context['filter'].qs:
            self.assertIn(label, task.labels.all())

    def test_task_filter_self_tasks(self):
        """Тест фильтрации только своих задач"""
        self.client.force_login(self.user1)
        
        response = self.client.get(
            reverse('tasks_list'),
            {'self_tasks': 'on'}
        )
        self.assertEqual(response.status_code, 200)
        for task in response.context['filter'].qs:
            self.assertEqual(task.author, self.user1)


class LabelTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)

    def test_labels_list_not_authenticated(self):
        """Тест: список меток недоступен без авторизации"""
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 302)

    def test_labels_list_authenticated(self):
        """Тест: список меток доступен авторизованным"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label1.name)

    def test_label_create(self):
        """Тест создания метки"""
        self.client.force_login(self.user1)
        labels_count = Label.objects.count()

        response = self.client.post(reverse('label_create'), {
            'name': 'Новая метка',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), labels_count + 1)

    def test_label_update(self):
        """Тест обновления метки"""
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse('label_update', args=[self.label1.pk]),
            {'name': 'Обновлённая метка'}
        )
        self.assertEqual(response.status_code, 302)
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, 'Обновлённая метка')

    def test_label_delete(self):
        """Тест удаления метки"""
        self.client.force_login(self.user1)
        label = Label.objects.create(name='Метка для удаления')
        labels_count = Label.objects.count()

        response = self.client.post(
            reverse('label_delete', args=[label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), labels_count - 1)

    def test_label_delete_in_use(self):
        """Тест попытки удаления метки, связанной с задачей"""
        self.client.force_login(self.user1)
        labels_count = Label.objects.count()

        response = self.client.post(
            reverse('label_delete', args=[self.label1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), labels_count)
