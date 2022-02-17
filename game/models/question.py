from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=128, null=True, default=None)
    
    round = models.ForeignKey(to='Round', on_delete=models.CASCADE)
    author = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING, related_name='asked_questions')
    respondent = models.ForeignKey(to='Player', on_delete=models.DO_NOTHING, related_name='answered_questions', null=True, default=None)
    answer = models.OneToOneField(to='Answer', on_delete=models.CASCADE, related_name='question')
