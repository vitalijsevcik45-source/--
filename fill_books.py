import os
import django

# Налаштовуємо оточення Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from mainapp.models import Category, Product


def populate():
    print("🚀 Запуск генерації асортименту книг...")

    # Створюємо або отримуємо категорії
    cat_prog, _ = Category.objects.get_or_create(name="Програмування")
    cat_scifi, _ = Category.objects.get_or_create(name="Фантастика")
    cat_psy, _ = Category.objects.get_or_create(name="Психологія та Розвиток")

    books_data = [
        {
            "title": "Django 5 для професіоналів",
            "category": cat_prog,
            "price": 650,
            "description": "Найкраще практичне керівництво з побудови складних, швидких та безпечних веб-сайтів на Python та Django.\n\nПідійде як для початківців, так і для тих, хто вже має базовий досвід розробки.",
        },
        {
            "title": "Чистий Код (Clean Code)",
            "category": cat_prog,
            "price": 480,
            "description": "Легендарна книга Роберта Мартіна. Вона навчить вас писати зрозумілий, гнучкий, охайний та професійний код, який легко підтримувати іншим розробникам.",
        },
        {
            "title": "Дюна (Колекційне видання)",
            "category": cat_scifi,
            "price": 390,
            "description": "Шедевр світової фантастики від Френка Герберта. Неймовірна історія про пустельну планету Арракіс, таємничі прянощі, гігантських піщаних хробаків та запеклу боротьбу за владу в галактиці.",
        },
        {
            "title": "Автостопом по галактиці",
            "category": cat_scifi,
            "price": 280,
            "description": "Неймовірно смішна, іронічна та культова фантастична подорож Артура Дента автостопом всесвітом після того, як Землю було знищено задля побудови міжгалактичного гіперпросторового шосе.",
        },
        {
            "title": "Атомні звички",
            "category": cat_psy,
            "price": 320,
            "description": "Проста, покрокова та перевірена часом інструкція, як легко позбутися поганих щоденних звичок та сформувати хороші за допомогою крихітних змін у поведінці.",
        },
        {
            "title": "Мислення швидке й повільне",
            "category": cat_psy,
            "price": 450,
            "description": "Книга нобелівського лауреата Деніела Канемана, яка детально та на життєвих прикладах пояснює, як насправді працює наш мозок, дві системи мислення та як ми приймаємо рішення.",
        }
    ]

    for data in books_data:
        product, created = Product.objects.get_or_create(
            title=data["title"],
            defaults={
                "category": data["category"],
                "price": data["price"],
                "description": data["description"]
            }
        )
        if created:
            print(f"✅ Додано книгу: {product.title}")
        else:
            print(f"🔄 Книга вже існує в базі: {product.title}")

    print("\n🎉 Асортимент та категорії успішно оновлено!")


if __name__ == '__main__':
    populate()