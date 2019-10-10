from decimal import Decimal
from django.conf import settings
from shop.models import Product


# 此类负责管理购物车，同时该购物车需要request对象进行初始化
class Cart(object):
    def __init__(self, request):
        """
        初始化购物车
        """
        # 下面的语句用来存储当前会话，使其可以访问cart类中的其他的方法
        self.session = request.session
        # 从当前会话中获取购物车
        cart = self.session.get(settings.CART_SESSION_ID)
        # 如果购物车为空，则创建一个新的空购物车缓存
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        # 这里的self.cart中的cart是session名称
        self.cart = cart

    # 在这里期望购物车字典使用商品ID作为键，以及一个包含数量和价格的字典作为每个键值，依据此方式
    # 可以确保某件商品不会被重复添加到购物车中，当添加同样的商品时，仅仅只需要修改该商品的数量即可

    def add(self, product, quantity=1, update_quantity=False):
        """
        此方法用来添加商品到购物车或者更新购物车中的商品的数量
        :param product: 表示购物车中添加或更新的product实例
        :param quantity: 商品数量
        :param update_quantity: 定义为一个布尔值，表示当前数量是否需要利用给定的量值进行更新（True）
        或者新量值是否需要加入现有的量值中（False）
        :return:
        """
        # 因为json仅支持字符串，因而需要将商品id转换为字符串
        product_id = str(product.id)
        # 这里的self.cart中的cart指的是session的名称
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        # if update_quantity = True:
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        # 将修改后的session保存
        self.save()

    def save(self):
        # 将session标记为modified，来表明其已经保存，这将通知Django，该会话已经发生改变且需要保存
        self.session.modified = True

    def remove(self, product):
        """
        从购物车中移除商品
        :param self:
        :param product: 表示购物车中添加或更新的product实例
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        迭代购物车中的对象，并且从数据库中取出商品
        :param self:
        :return:
        """
        # 取出cart中的所有的键
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            # 将整件商品存储到session中，这样是可以避免加入购物车的商品价格变化而与源数据中的价格不一致
            cart[str(product.id)]['product'] = product
        # 遍历购物车中的各个条目，将其价格转换成小数，并将total_price属性添加至各个条目中
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # 遍历购物车，并将购物车中的所有数量进行相加
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # 遍历购物车并计算总价格
        return sum(Decimal(item['price']) * Decimal(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
