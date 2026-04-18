from Hangy.models import Product
from typing import List, Tuple
from Hangy import PAGE_SIZE

class ProductService:
    def load_products(
            self,
            kw: str = None,
            page: int = 1,
            page_size: int = PAGE_SIZE
    ) -> Tuple[List[Product], int]:
        try:
            if page < 1:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = PAGE_SIZE

            query = Product.query

            if kw:
                clean_kw = kw.strip()
                if len(clean_kw) > 0:
                    query = query.filter(Product.name.contains(clean_kw))

            start = (page - 1) * page_size
            total = query.count()
            products = query.offset(start).limit(page_size).all()

            return products, total

        except Exception as e:
            print(f"Lỗi khi load danh sách sản phẩm: {e}")
            return [], 0

    def get_product_by_id(self, product_id: int) -> Product | None:
        try:
            if not product_id or product_id <= 0:
                return None

            product = Product.query.get(product_id)
            if not product:
                print(f"Sản phẩm ID {product_id} không tồn tại.")

            return product
        except Exception as e:
            print(f"Lỗi khi lấy chi tiết sản phẩm: {e}")
            return None


product_service = ProductService()