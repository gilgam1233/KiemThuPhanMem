from Hangy.models import Product

def load_products(kw=None, page=1, page_size=6):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))
    start = (page - 1) * page_size

    total = query.count()

    courses = query.offset(start).limit(page_size).all()

    return courses, total
