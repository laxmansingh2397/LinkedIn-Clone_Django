from django.contrib import admin
from .models import Profile,Education,Experience,Skill,UserSkill,Post,Comment,Like,Connection,Message,Job,JobApplication

# Register your models here.

admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Connection)
admin.site.register(Message)
admin.site.register(Job)
admin.site.register(JobApplication)
