from django.db import models

class Answer(models.Model):
    statement = models.CharField(max_length=200)

    class Admin: pass

    def __unicode__(self):
        return unicode(self.statement)

class Question(models.Model):
    problem = models.CharField(max_length=200)
    answers = models.ManyToManyField(Answer)

    class Admin: pass

    def __unicode__(self):
        return unicode(self.problem)

class Page(models.Model):
    name = models.CharField(max_length=50)
    questions = models.ManyToManyField(Question)

    class Meta:
        verbose_name_plural = 'pages'

    class Admin: pass

    def __unicode__(self):
        return unicode(self.name)
