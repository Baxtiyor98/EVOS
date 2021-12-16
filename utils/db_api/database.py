from gino import Gino
from data.config import DB_HOST, DB_NAME, DB_PASS,DB_USER

db = Gino()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    username = db.Column(db.String)
    telegram_id = db.Column(db.String)
    phone_number = db.Column(db.String)
    location = db.Column(db.String)

class Categories(db.Model):
    __tablename__ = "categories"
    
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    category_description = db.Column(db.String)

class Products(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    product_name = db.Column(db.String)
    price = db.Column(db.String)
    photo = db.Column(db.String)

class Order_products(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.telegram_id'))
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.String)

class DBCommands():

    async def get_users(self):
        users= await User.query.gino.all()
        return users
    async def create_user(tg_id,fname,phone,username,location):
        await User.create(full_name=fname,phone_number=phone,username=username,location=location,telegram_id=tg_id)
    
    async def update_location(self,id,item):
        user = await User.query.where(User.telegram_id == str(id)).gino.first()
        await user.update(location=item).apply()
    
    async def update_phone(self,id,item):
        user = await User.query.where(User.telegram_id == str(id)).gino.first()
        await user.update(phone_number=item).apply()
    
    async def update_name(self,id,item):
        user = await User.query.where(User.telegram_id == str(id)).gino.first()
        await user.update(full_name=item).apply()
        
    async def get_category(self):
        categories = await Categories.query.gino.all()
        return categories
        
    async def get_products(self):
        products= await Products.query.gino.all()
        return products
        
    async def get_price(self,name):
        name = name[1:]
        price= await Products.select('price').where(Products.product_name == name).gino.scalar()
        return price
    
    async def order(self,id,product_name,quantity,price):
        await Order_products.create(user_id=id,product_name=product_name,quantity=quantity,price=str(price))

    async def get_order(self,id):
        orders= await Order_products.query.where(Order_products.user_id == id).gino.all()
        return orders

    async def delete_order(self,id):
        await Order_products.delete.where(Order_products.order_id == int(id)).gino.status()
        
    async def clear_order(self,id):
        orders= await Order_products.query.where(Order_products.user_id == id).gino.all()
        return orders
async def create_db():
    # await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    # await db.gino.drop_all()
    # await db.gino.create_all()
