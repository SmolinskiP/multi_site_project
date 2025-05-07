# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, GalleryImage, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'image_preview')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview_large',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category')
        }),
        ('Obraz', {
            'fields': ('image', 'image_preview_large')
        }),
    )
    
    def image_preview(self, obj):
        """Miniaturka zdjęcia w liście"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                             obj.image.url)
        return "-"
    
    def image_preview_large(self, obj):
        """Większy podgląd zdjęcia w formularzu"""
        if obj.image:
            return format_html('<img src="{}" width="400" style="max-height: 300px; object-fit: contain;" />',
                             obj.image.url)
        return "-"
    
    image_preview.short_description = 'Podgląd'
    image_preview_large.short_description = 'Podgląd zdjęcia'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('subject', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    def has_add_permission(self, request):
        # Nie pozwalamy na dodawanie wiadomości przez panel admina
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Możesz tutaj zdecydować, czy chcesz pozwolić na usuwanie wiadomości
        return True
    
    # Akcja do oznaczania wiadomości jako przeczytane
    @admin.action(description="Oznacz wybrane wiadomości jako przeczytane")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    
    # Akcja do oznaczania wiadomości jako nieprzeczytane
    @admin.action(description="Oznacz wybrane wiadomości jako nieprzeczytane")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    
    actions = [mark_as_read, mark_as_unread]