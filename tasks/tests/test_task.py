from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from authentication.tests.factories.custom_user import CustomUserFactory
from tasks.tests.factories.task import TaskFactory


class TasksAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_1 = CustomUserFactory()
        self.user_2 = CustomUserFactory()
        self.task_1 = TaskFactory(user=self.user_1)
        self.task_2 = TaskFactory(user=self.user_2)

    def test_create_task(self):
        self.client.force_authenticate(self.user_1)
        data = {
            "title": "string",
            "description": "string",
            "completed": "true"
        }
        response = self.client.post(reverse("task-list"), format="json", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_without_description(self):
        self.client.force_authenticate(self.user_1)
        data = {
            "title": "string",
            "completed": "true"
        }
        response = self.client.post(reverse("task-list"), format="json", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_task(self):
        self.client.force_authenticate(self.user_1)
        response = self.client.get(reverse("task-list"))
        output = response.data

        self.assertEqual(output['results'][0]['title'], self.task_1.title)
        self.assertEqual(output['results'][0]['description'], self.task_1.description)

    def test_get_task_without_auth(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task(self):
        self.client.force_authenticate(self.user_1)
        data = {
            "title": "string update",
            "description": "string",
            "completed": "true"
        }
        response = self.client.put(reverse("task-detail", kwargs={'pk': 1}), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("string update", response.data['title'])

    def test_update_task_user_not_owner_task(self):
        self.client.force_authenticate(self.user_2)
        data = {
            "title": "string update",
            "description": "string",
            "completed": "true"
        }
        response = self.client.put(reverse("task-detail", kwargs={'pk': 1}), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
