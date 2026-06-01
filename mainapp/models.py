from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Назва книги")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото товару")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    rating = models.IntegerField(default=5, verbose_name="Оцінка (1-5)")
    comment = models.TextField(verbose_name="Коментар", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    # Зверни увагу: class Meta має рівно 4 пробіли від краю, як і поля вище!
    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email для розсилки")
    created_at = models.DateTimeField(auto_now_add=True)

    # Тут так само — посунь class Meta вліво, щоб було рівно 4 пробіли від краю
    class Meta:
        verbose_name = "Підписка"
        verbose_name_plural = "Підписки"

    def __str__(self):
        return self.email