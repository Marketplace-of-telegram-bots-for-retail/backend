import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model

from mixer.backend.django import mixer

from rest_framework.test import APITestCase

User = get_user_model()


