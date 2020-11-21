from django.contrib import admin
from .models import BlockInfo,KAMAZ,HeaderBlock,RegistrationBlock,SiteContent,Profile,HaveQuestionsBlock,SendQuestionBlock,Question


class SiteContentAdmin(admin.ModelAdmin):
    list_display=("id",'name')
    list_display_links=("id","name")


admin.site.register(BlockInfo)
admin.site.register(KAMAZ)
admin.site.register(HeaderBlock)
admin.site.register(RegistrationBlock)
admin.site.register(SiteContent,SiteContentAdmin)
admin.site.register(Profile)
admin.site.register(HaveQuestionsBlock)
admin.site.register(SendQuestionBlock)
admin.site.register(Question)





