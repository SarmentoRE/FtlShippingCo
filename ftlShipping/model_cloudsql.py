from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import synonym

builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START truck model]
class Truck(db.Model):
    __tablename__ = 'Truck'

    truckId = db.Column(db.Integer, primary_key=True)
    weightCapacity = db.Column(db.Numeric())
    inUse = db.Column(db.Numeric())
    type = db.Column(db.String(7))
    costPerMile = db.Column(db.Numeric())
    maxVolume = db.Column(db.Numeric())
    carrier = db.Column(db.String(30))
    id = synonym("truckId")

    def __repr__(self):
        return "<Truck(id='%i', carrier=%s)" % (self.truckId, self.carrier)
# [END truck model]


class Order(db.Model):
    __tablename__ = 'Orders'

    orderId = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric())
    destStreetName = db.Column(db.String(20))
    destStreetNumber = db.Column(db.Integer)
    destAptNumber = db.Column(db.String(10))
    destCity = db.Column(db.String(30))
    destState = db.Column(db.String(2))
    destZip = db.Column(db.Integer)
    originStreetName = db.Column(db.Integer)
    originStreetNumber = db.Column(db.Integer)
    originAptNumber = db.Column(db.String(10))
    originCity = db.Column(db.String(30))
    originState = db.Column(db.String(2))
    originZip = db.Column(db.Integer)
    volume = db.Column(db.Numeric())
    dateOrdered = db.Column(db.Date())
    orderStatus = db.Column(db.String(16))
    id = synonym("orderId")

    def __repr__(self):
        if self.destAptNumber is None:
            return "<Order(id='%i'\nDestination Address:\n%i %s\n%s, %s, %i\n\nStatus='%s')" % (self.orderId, self.destStreetNumber, self.destStreetName, self.destCity, self.destState, self.destZip, self.orderStatus)
        return "<Order(id='%i'\nDestination Address:\n%i %s\n%s\n%s, %s, %i\n\nStatus='%s')" % (self.orderId, self.destStreetNumber, self.destStreetName, self.destAptNumber, self.destCity, self.destState, self.destZip, self.orderStatus)


class Item(db.Model):
    __tablename__ = 'Item'

    itemId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30))
    stock = db.Column(db.Integer)
    category = db.Column(db.String(30))
    weight = db.Column(db.Numeric())
    volume = db.Column(db.Numeric())
    id = synonym("itemId")

    def __repr__(self):
        return "<Item(id='%i' name='%s' stock='%i' weight='%f')" % (self.itemId, self.name, self.stock, self.weight)


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Truck.query
             .order_by(Truck.costPerMile)
             .limit(limit)
             .offset(cursor))
    trucks = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(trucks) == limit else None
    return (trucks, next_page)
# [END list]


# [START read]
def read(id):
    result = Truck.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    truck = Truck(**data)
    db.session.add(truck)
    db.session.commit()
    return from_sql(truck)
# [END create]


# [START update]
def update(data, id):
    truck = Truck.query.get(id)
    for k, v in data.items():
        setattr(truck, k, v)
    db.session.commit()
    return from_sql(truck)
# [END update]


def delete(id):
    Truck.query.filter_by(id=id).delete()
    db.session.commit()


# [START list]
def listItem(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .order_by(Item.itemId)
             .limit(limit)
             .offset(cursor))
    items = builtin_list(map(from_sql, query.all()))
    print("query %s" % query)
    next_page = cursor + limit if len(items) == limit else None
    return (items, next_page)
# [END list]


# [START read]
def readItem(id):
    result = Item.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def createItem(data):
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return from_sql(item)
# [END create]


# [START update]
def updateItem(data, id):
    item = Item.query.get(id)
    for k, v in data.items():
        setattr(item, k, v)
    db.session.commit()
    return from_sql(item)
# [END update]


def deleteItem(id):
    Item.query.filter_by(id=id).delete()
    db.session.commit()


# [START list]
def listOrder(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Order.query
             .order_by(Order.orderId)
             .limit(limit)
             .offset(cursor))
    order = builtin_list(map(from_sql, query.all()))
    print("query %s"%query)
    next_page = cursor + limit if len(order) == limit else None
    return (order, next_page)
# [END list]


# [START read]
def readOrder(id):
    result = Order.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def createOrder(data):
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return from_sql(order)
# [END create]


# [START update]
def updateOrder(data, id):
    order = Order.query.get(id)
    for k, v in data.items():
        setattr(order, k, v)
    db.session.commit()
    return from_sql(order)
# [END update]


def deleteOrder(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
