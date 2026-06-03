from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review, Newsletter, Order, OrderItem


# ==================== ГОЛОВНА ТА КАТЕГОРІЇ ====================

def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    if request.method == 'POST' and 'email_subscribe' in request.POST:
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
        return redirect('home')

    context = {
        'categories': categories,
        'products': products,
        'text_content': 'Вітаємо у нашій книжковій крамниці! Тут ви знайдете найкращі книги.'
    }
    return render(request, 'mainapp/home.html', context)


def category_view(request, category_id):
    categories = Category.objects.all()
    current_category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=current_category)
    context = {
        'categories': categories,
        'current_category': current_category,
        'products': products
    }
    return render(request, 'mainapp/category.html', context)


def product_view(request, product_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)

    if request.method == 'POST' and 'submit_rating' in request.POST:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        if rating:
            Review.objects.create(product=product, rating=int(rating), comment=comment)
        return redirect('product_detail', product_id=product.id)

    average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating:
        average_rating = round(average_rating, 1)
    else:
        average_rating = "Немає оцінок"

    context = {
        'categories': categories,
        'product': product,
        'average_rating': average_rating,
        'reviews': product.reviews.all().order_by('-created_at')
    }
    return render(request, 'mainapp/product_detail.html', context)


# ==================== ПРОФІЛЬ ТА АВТЕНТИФІКАЦІЯ ====================

def register_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'mainapp/register.html', {'categories': categories})


def login_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'mainapp/login.html', {'categories': categories})


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'mainapp/profile.html', {'categories': categories})


# ==================== РОБОТА З КОШИКОМ ====================

def cart_detail_view(request):
    categories = Category.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item_data['quantity']
        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    context = {
        'categories': categories,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'mainapp/cart.html', context)


def cart_add_view(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str not in cart:
        cart[product_id_str] = {'quantity': 1}
    else:
        cart[product_id_str]['quantity'] += 1

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_remove_view(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_clear_view(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_detail')


# ==================== ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ====================

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')

        # Вираховуємо суму на основі актуальних цін з бази даних (у типі Decimal)
        total_price = 0
        order_items_to_create = []

        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item_data['quantity']
            total_price += product.price * quantity

            # Тимчасово зберігаємо дані для створення книг у замовленні
            order_items_to_create.append({
                'product': product,
                'price': product.price,
                'quantity': quantity
            })

        # Створюємо одне головне замовлення в базі даних
        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            phone=phone,
            total_price=total_price
        )

        # Тепер прив'язуємо всі книги з кошика до цього замовлення
        for item in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Очищаємо кошик у сесії
        request.session['cart'] = {}

        # Рендеримо сторінку успіху
        return render(request, 'mainapp/order_success.html', {'order': order})

    return redirect('cart_detail')