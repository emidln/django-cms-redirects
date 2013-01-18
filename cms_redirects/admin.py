from django.contrib import admin
from cms_redirects.models import CMSRedirect

class CMSRedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'page', 'page_site', 'site', 'actual_response_code', 'soft')
    list_filter = ('site', 'soft',)
    search_fields = ('old_path', 'new_path', 'page__title_set__title')
    radio_fields = {'site': admin.VERTICAL}
    fieldsets = [
        ('Source', {
            "fields": ('site','old_path',)
        }),
        ('Destination', {
            "fields": ('new_path','page', 'response_code',)
        }),
        ('Soft Option', {
            "fields": ('soft', 'soft_timeout_seconds', 'soft_erase_history', 'message',),
        }),
    ]

admin.site.register(CMSRedirect, CMSRedirectAdmin)
