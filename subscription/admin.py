from django.contrib import admin

from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'plan_type', 'description')
    search_fields = ('name', 'plan_type')
    list_filter = ('plan_type',)

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'last_renewed_at')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('is_active', 'plan', 'user')
    readonly_fields = ('start_date', 'last_renewed_at')  # Make start and renewal times read-only

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
