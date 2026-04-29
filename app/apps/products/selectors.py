from apps.products.models import Product


def get_active_products():
    return Product.objects.filter(is_deleted=False)


def get_visible_products_for_user(user):
    qs = get_active_products()

    if user.role == "ADMIN":
        return qs

    if user.role == "STAFF":
        return qs

    return qs.filter(is_active=True)


def get_product_by_id(product_id):
    return get_active_products().get(id=product_id)


def search_products(query):
    return get_active_products().filter(
        name__icontains=query
    ) | get_active_products().filter(description__icontains=query)


def filter_products_by_price(min_price=None, max_price=None):
    qs = get_active_products()

    if min_price is not None:
        qs = qs.filter(price__gte=min_price)

    if max_price is not None:
        qs = qs.filter(price__lte=max_price)

    return qs
