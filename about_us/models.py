from django.db import models
import re

# Create your models here.

class AboutUs(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'About Us'

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        # Capitalize first letter of question
        if self.question:
            self.question = self.question[:1].upper() + self.question[1:]

        # Capitalize first letter of each sentence in answer
        if self.answer:
            # split by sentence endings (.!?)
            sentences = re.split(r'([.!?]\s*)', self.answer)
            # capitalize first character of each sentence
            self.answer = ''.join([s.capitalize() for s in sentences])

        super().save(*args, **kwargs)