from django.contrib import admin
from .models import Subject, PracticeRecord, GroupAssign, MessageRecord, EstimationRecord, FormalRecord, UnderstandingSurvey, Defendant

# Register your models here.
admin.site.register(Subject)
admin.site.register(PracticeRecord)
admin.site.register(FormalRecord)
admin.site.register(GroupAssign)
admin.site.register(MessageRecord)
admin.site.register(EstimationRecord)
admin.site.register(UnderstandingSurvey)
admin.site.register(Defendant)