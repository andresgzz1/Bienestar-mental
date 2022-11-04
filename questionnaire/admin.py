from django.contrib import admin


from  embed_video.admin  import  AdminVideoMixin
from .models  import  Link_techniques
#Register your models here.

class  tutorialAdmin(AdminVideoMixin, admin.ModelAdmin):
	pass

admin.site.register(Link_techniques, tutorialAdmin)
# Register your models here.
