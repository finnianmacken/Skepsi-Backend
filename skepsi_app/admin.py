from django.contrib import admin
from .models import Annotation, Paper, User, Profile, Topic, Reference, Score, Figure, Table
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Adds information from the Profile model to the User model in the admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Representing Papers as an inline field for Topics in Django admin
class PaperInlineAdmin(admin.TabularInline):
    model = Paper


class ReferenceInlineAdmin(admin.TabularInline):
    model = Reference


class TopicAdmin(admin.ModelAdmin):
    inlines = [PaperInlineAdmin,]


class PaperAdmin(admin.ModelAdmin):
    inlines = [ReferenceInlineAdmin, ]


class ScoreInlineAdmin(admin.TabularInline):
    model = Score


class AnnotationAdmin(admin.ModelAdmin):
    inlines = [ScoreInlineAdmin, ]

admin.site.register(Reference)
admin.site.register(Table)
admin.site.register(Score)
admin.site.register(Figure)
admin.site.register(Profile)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Topic, TopicAdmin)
