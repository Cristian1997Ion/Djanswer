from django.db import models

class Answer(models.Model):
    text = models.CharField(max_length=128, null=True, default=None)
    
    question = models.OneToOneField(to='Question', on_delete=models.CASCADE, related_name='answer')
    player = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING)
