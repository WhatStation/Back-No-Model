from django.db import models

class Rate(models.Model) :
    rating = models.PositiveSmallIntegerField('RATING') # 별점, 비어있을수없음
    comment = models.TextField('COMMENT', max_length=300)
    password = models.CharField('password', max_length=10)

    @property
    def short_comment(self) :
        return self.comment[:10]

    def __str__(self) :
        return self.short_comment