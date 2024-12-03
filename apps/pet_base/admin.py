from django.utils.html import format_html
from django.contrib import admin
from apps.pet_base import models


@admin.register(models.Pet)
class PetAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = (
    "name", "animal_type", "breed", "gender", "age", "owner_link", "get_owner_phone", "created_at")

    def owner_link(self, obj):
        # Формируем ссылку на страницу владельца
        return format_html('<a href="/admin/pet_base/owner/{}/change/">{}</a>', obj.owner.id, obj.owner.name)

    owner_link.short_description = 'Владелец'

    list_filter = ("animal_type", "breed")
    search_fields = ("name", "owner__name", "owner__phone")

    def get_owner_name(self, obj):
        return obj.owner.name
    get_owner_name.short_description = "Владелец"

    def get_owner_phone(self, obj):
        return obj.owner.phone
    get_owner_phone.short_description = "Телефон владельца"


@admin.register(models.Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'get_pet_name')

    def get_pet_name(self, obj):
        pets = obj.pets.all()  # Получаем всех питомцев, связанных с владельцем
        return ', '.join([pet.name for pet in pets]) if pets else 'Без питомцев'

    get_pet_name.short_description = 'Питомцы'


@admin.register(models.AnimalType)
class AnimaTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
