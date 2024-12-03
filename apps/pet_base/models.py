from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


class AnimalType(models.Model):
    """
    Модель для хранения видов животных
    """
    name = models.CharField(
        verbose_name="Вид животного",
        max_length=50,
        unique=True,
        help_text="Название вида животного, например: собака, кошка и т.д."
    )

    class Meta:
        verbose_name = "вид животного"
        verbose_name_plural = "виды животных"

    def __str__(self):
        return self.name


class Owner(models.Model):
    """
    Модель для хранения владельцев животных
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Некорректный формат ввода"
    )

    name = models.CharField(
        verbose_name="ФИО",
        max_length=100,
        help_text="ФИО полностью"
    )
    phone = models.CharField(
        verbose_name="Номер телефона",
        validators=[phone_regex],
        max_length=17,
        blank=True, null=True,
        help_text="Номер телефона в формате: +799999999"
    )

    class Meta:
        verbose_name = "владелец"
        verbose_name_plural = "владельцы"

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Pet(models.Model):
    """
    Модель для хранения информации о питомцах
    """
    class AnimalGender(models.TextChoices):
        MALE = 'M', 'мужской'
        FEMALE = 'F', 'женский'

    name = models.CharField(
        verbose_name="Кличка",
        max_length=50,
    )
    animal_type = models.ForeignKey(
        AnimalType,
        on_delete=models.PROTECT,
        related_name="pets",
        verbose_name="Вид животного",
        help_text="Выберите вид животного"
    )
    breed = models.CharField(
        verbose_name="Порода",
        max_length=50,
        blank=True, null=True,
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=1,
        choices=AnimalGender.choices,
        default=AnimalGender.MALE,
    )
    age = models.IntegerField(
        verbose_name="Возраст",
        blank=True, null=True,
        validators=[MinValueValidator(0)],
        help_text="Количество полных лет"
    )
    weight = models.FloatField(
        verbose_name="Вес(кг)",
        blank=True, null=True,
        validators=[MinValueValidator(0.01)],
    )
    vaccinations = models.TextField(
        verbose_name="Вакцинации",
        blank=True, null=True,
        help_text="Укажите тип и название прививки, год вакцинации"
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="pets",
        verbose_name="Владелец",
        help_text="ФИО владельца"
    )
    notes = models.TextField(
        verbose_name="Дополнительная информация",
        max_length=500,
        blank=True, null=True,
        help_text="Особенности поведения питомца, возможные проблемы"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        help_text="Генерируется автоматически",
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
        help_text="Обновляется автоматически",
    )

    class Meta:
        verbose_name = "питомец"
        verbose_name_plural = "питомцы"

    def __str__(self):
        return f"{self.name} ({self.animal_type.name}), возраст: {self.age} лет. Владелец - {self.owner}."

# TODO можно реализовать возможность добавления фото питомца
