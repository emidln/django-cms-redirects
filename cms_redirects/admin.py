from django.contrib import admin
from cms_redirects.models import CMSRedirect

def make_enabled(modeladmin, request, queryset):
    queryset.update(enabled=True)
make_enabled.short_description = 'Enable selected redirects'

def make_disabled(modeladmin, request, queryset):
    queryset.update(enabled=False)
make_disabled.short_description = 'Disabled selected redirects'

class CMSRedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'enabled', 'page', 'page_site', 'site', 'actual_response_code', 'soft')
    list_filter = ('site', 'soft', 'enabled')
    search_fields = ('old_path', 'new_path', 'page__title_set__title')
    radio_fields = {'site': admin.VERTICAL}
    fieldsets = [
        ('Enabled', {
            'fields': ('enabled',)
        }),
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
    actions = [make_enabled, make_disabled]

admin.site.register(CMSRedirect, CMSRedirectAdmin)
