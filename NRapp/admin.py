from django.contrib import admin
from .models import Category, Product, ProductImage, Inquiry


# ================= CATEGORY =================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


# ================= IMAGE INLINE =================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    readonly_fields = ('created_at',)


# ================= PRODUCT =================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'is_active',
        'created_at'
    )

    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

    inlines = [ProductImageInline]

    # ⭐ ACTIONS
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected products as Active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected products as Inactive"


# ================= PRODUCT IMAGE =================
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'created_at')
    search_fields = ('product__name',)


# ================= INQUIRY CRM =================
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'phone',
        'email',
        'status',           # ✅ REQUIRED for list_editable
        'colored_status',   # 🎨 UI display
        'priority',
        'is_read',
        'created_at'
    )

    list_filter = ('status', 'priority', 'is_read', 'created_at')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)

    list_editable = ('status', 'priority', 'is_read')
    readonly_fields = ('created_at',)

    # 🎨 Colored Status Display
    def colored_status(self, obj):
        if obj.status == 'new':
            return "🔴 New"
        elif obj.status == 'contacted':
            return "🟡 Contacted"
        return "🟢 Closed"
    colored_status.short_description = "Status View"

    # ⭐ Bulk Actions
    actions = ['mark_read', 'mark_unread', 'mark_closed']

    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)

    def mark_closed(self, request, queryset):
        queryset.update(status='closed')