from flask import Flask, request, jsonify
from models import db,User, Product, Order
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'], stock=data.get('stock', 0))
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name}), 201




@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data['user_id']
    total = data['total']

    order = Order(user_id=user_id,total=total)
    db.session.add(order)
    db.session.commit()
    return jsonify({"order_id": order.id}), 201

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    u_id = data['id']
    username = data['username']
    email = data['email']

    user=User(id=u_id,username=username,email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id}), 201




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
