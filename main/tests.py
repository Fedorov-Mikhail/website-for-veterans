from django.core import mail
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse


class IssueReportRateLimitTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(HTTP_HOST='localhost')
        self.url = reverse('main:submit_issue_report')
        self.payload = {
            'problem_type': 'fact',
            'message': 'На странице указан некорректный тестовый текст для проверки формы.',
            'contact': 'tester@example.com',
            'consent': 'true',
        }

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='test@example.com',
        ISSUE_REPORT_RECIPIENT='ivan.kupreev03@gmail.com',
        ISSUE_REPORT_RATE_LIMIT=2,
        ISSUE_REPORT_RATE_LIMIT_WINDOW=60,
    )
    def test_issue_report_rate_limit_blocks_extra_posts(self):
        for _ in range(2):
            response = self.client.post(self.url, self.payload)
            self.assertEqual(response.status_code, 302)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 2)
