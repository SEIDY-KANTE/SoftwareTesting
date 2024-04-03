from django.db import models


class Metrics(models.Model):

    ClassName = models.CharField(primary_key=True, max_length=70)
    JavaDocLines = models.IntegerField()
    OtherComments = models.IntegerField()
    CodeLines = models.IntegerField()
    Loc = models.IntegerField()
    FunctionLines = models.IntegerField()
    CommentDeviation = models.DecimalField(max_digits=5, decimal_places=2)
