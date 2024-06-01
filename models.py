from django.db import models
from django.urls import reverse
from accounts.models import CustomUser  # Import your custom user model

class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Priority(models.Model):
    level = models.CharField(max_length=20)

    def __str__(self):
        return self.level

class Post(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reporter_posts'
    )
    assignee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assigned_posts',
        blank=True, null=True
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('to_do', 'To Do'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('draft', 'Draft')
        ],
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", args=[self.id])
