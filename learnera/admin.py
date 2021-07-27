from django.contrib import admin
from .models import allcourse,profile,Orders,contribution,Contact

# Register your models here.


class allcourseAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/learnera.js",)


admin.site.register(allcourse,allcourseAdmin)
admin.site.register(profile)
admin.site.register(Orders)
admin.site.register(contribution)
admin.site.register(Contact)

