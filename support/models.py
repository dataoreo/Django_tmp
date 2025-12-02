from django.db import models


class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    # 대분류-중분류 구조를 위해 자기 자신(self)을 참조
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_categories')
    depth = models.IntegerField(default=1)  # 1: 대분류, 2: 중분류

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='items')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question