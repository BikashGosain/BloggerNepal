from django.db import models
import re

class AboutUs(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About Us"
        ordering = ["created_at"]

    def __str__(self):
        return self.question

    def clean(self):
        if self.question:
            self.question = self.question.capitalize()

        if self.answer:
            sentences = re.split(r'([.!?]\s*)', self.answer)
            self.answer = ''.join(s.capitalize() for s in sentences)
