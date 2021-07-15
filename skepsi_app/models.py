from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isUser = models.BooleanField(default=False)
    isScientist = models.BooleanField(default=False)
    isDomainExpert = models.BooleanField(default=False)
    orcid = models.CharField(max_length=30, default='')


class Topic(models.Model):
    header = models.CharField(max_length=40)
    domain = models.CharField(max_length=75)
    slug = models.SlugField(max_length=100, default="")

    def __str__(self):
        return f'{self.header}'

class Paper(models.Model):
    title = models.CharField(max_length=2000)
    authors = models.CharField(max_length=2000)
    abstract = models.TextField(max_length=10000, default="")
    created_date = models.CharField(max_length=500, default="")
    citationMLA = models.TextField(max_length=2000, default="")
    citationAPA = models.TextField(max_length=2000, default="")
    citationChicago = models.TextField(max_length=2000, default="")
    md = models.TextField(max_length=50000, default="")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='papers', default="")

    def __str__(self):
        return f'{self.title} [ID: {self.id}]'


class Reference(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE,
                              related_name='references', default=1)
    authors = models.TextField(max_length=1000)
    title = models.TextField(max_length=2000, default="")
    citation = models.TextField(max_length=2000, default="", blank=True)
    paperOrder = models.IntegerField(default=1)

    class Meta:
        unique_together = ('paper', 'paperOrder')

    def __str__(self):
        return f"{self.title} [Paper: {self.paper.title}, {self.paperOrder}]"


class Figure(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='figures')
    image = models.ImageField(upload_to="media/")
    name = models.CharField(max_length=2500, default="")
    figure_number = models.IntegerField(default=1)
    caption = models.TextField(max_length=50000, default="")

    def __str__(self):
        return self.image.name


POSITION_CHOICES = (
    ('positive', 'positive'),
    ('negative', 'negative')
)


class Annotation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='annotations')

    quote = models.TextField(blank=True)
    content = models.TextField(blank=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE,
                             related_name='annotations',
                             blank=True,
                             null=True,
                             default=None)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name='children')
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='positive'
    )
    start = models.IntegerField(blank=True, default=0)
    stop = models.IntegerField(blank=True, default=0)

    @property
    def children_dictionary(self):
        children = self.children.values()
        children_list = [entry for entry in children]
        return children_list

    def __str__(self):
        return f'{self.quote} [{self.author.username}, ID: {self.id}], [Paper: {self.paper}]'


SCORE_CHOICES = (
    ('Validity', 'Validity'),
    ('Novelty', 'Novelty'),
    ('Domain Importance', 'Domain Importance')
)


class Score(models.Model):
    score = models.CharField(
        max_length=100,
        choices=SCORE_CHOICES,
        default='Validity',
        null=True,
        blank=True,
    )
    explanation = models.TextField(max_length=10000)
    annotation = models.ForeignKey(Annotation,
                                   on_delete=models.CASCADE,
                                   related_name='scores')

    def __str__(self):
        return f'{self.score} on Annotation #{self.annotation.id}'
