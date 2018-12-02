from ftlShipping import get_model
from flask import Blueprint, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)


@crud.route("/")
def home():
    return render_template("Home.html")


@crud.route("/trucks")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    trucks, next_page_token = get_model().list(cursor=token)

    return render_template(
        "Trucklist.html",
        truck=trucks,
        next_page_token=next_page_token)


@crud.route('trucks/<id>')
def view(id):
    truck = get_model().read(id)
    orders = get_model().readDelivery(id)
    return render_template("Truckview.html", truck=truck, orders=orders)


@crud.route('trucks/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        truck = get_model().create(data)

        return redirect(url_for('.view', id=truck['id']))

    return render_template("Truckform.html", action="Add", truck={})


@crud.route('trucks/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    truck = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        truck = get_model().update(data, id)

        return redirect(url_for('.view', id=truck['id']))

    return render_template("Truckform.html", action="Edit", truck=truck)


@crud.route('trucks/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))


# Begin orders
@crud.route("/orders")
def listOrders():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    orders, next_page_token = get_model().listOrder(cursor=token)

    return render_template(
        "Orderlist.html",
        order=orders,
        next_page_token=next_page_token)


@crud.route('orders/<id>/ship')
def shipOrder(id):
    truck = get_model().findTrucks(id)
    order = get_model().readOrder(id)
    return render_template("Trucklist.html", truck=truck, action="ship", order=order)


@crud.route('orders/<id>')
def viewOrders(id):
    order = get_model().readOrder(id)
    item = get_model().readItemsOrdered(id)
    return render_template("Orderview.html", order=order, item=item)


@crud.route('orders/add', methods=['GET', 'POST'])
def addOrders():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        order = get_model().createOrder(data)

        return redirect(url_for('.viewOrders', id=order['id']))

    return render_template("Orderform.html", action="Add", order={})


# [END add]


@crud.route('orders/<id>/edit', methods=['GET', 'POST'])
def editOrders(id):
    order = get_model().readOrder(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        print(data)
        order = get_model().updateOrder(data, id)

        return redirect(url_for('.viewOrders', id=order['id']))

    return render_template("Orderform.html", action="Edit", order=order)


@crud.route('orders/<id>/delete')
def deleteOrders(id):
    get_model().deleteOrder(id)
    return redirect(url_for('.listOrders'))


# Begin Item
@crud.route("/item")
def listItem():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    items, next_page_token = get_model().listItem(cursor=token)

    return render_template(
        "Itemlist.html",
        items=items,
        next_page_token=next_page_token)


@crud.route('item/<id>')
def viewItem(id):
    item = get_model().readItem(id)
    return render_template("Itemview.html", item=item)


@crud.route('item/add', methods=['GET', 'POST'])
def addItem():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        item = get_model().createItem(data)

        return redirect(url_for('.viewItem', id=item['id']))

    return render_template("Itemform.html", action="Add", item={})


@crud.route('item/<id>/edit', methods=['GET', 'POST'])
def editItem(id):
    item = get_model().readItem(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        item = get_model().updateItem(data, id)

        return redirect(url_for('.viewItem', id=item['id']))

    return render_template("Itemform.html", action="Edit", item=item)


@crud.route('item/<id>/delete')
def deleteItem(id):
    get_model().deleteItemk(id)
    return redirect(url_for('.listItem'))


@crud.route('trucks/deliver/<truckId>/<orderId>')
def addItemToTruck(truckId, orderId):
    get_model().createDelivery(truckId, orderId)
    order = get_model().readOrder(orderId)
    order['orderStatus'] = "Shipped"
    get_model().updateOrder(order, orderId)
    return redirect(url_for('.listOrders'))


@crud.route('trucks/<truckId>/ship')
def shipItems(truckId):
    truck = get_model().read(truckId)
    truck['inUse'] = 1;
    get_model().update(truck, truckId)
    get_model().deliverItems(truckId)
    return redirect(url_for('.list'))


@crud.route('orders/<orderId>/addItems', methods=['GET', 'POST'])
def addItemsToOrder(orderId):
    order = get_model().readOrder(orderId)
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        dataObj = []
        tempObj = {}
        odd = True
        for key, value in data.items():
            if odd:
                tempObj['amount'] = value
                odd = False
            else:
                tempObj['itemId'] = value
                dataObj.append(tempObj)
                tempObj = {}
                odd = True
        for item in dataObj:
            if item['amount'] == '' or item['amount'] == '0':
                continue
            get_model().addItemsOrdered(item['itemId'], orderId, item['amount'])

    items, next_page_token = get_model().listItem(cursor=token)
    return render_template(
        "Itemlist.html", items=items, next_page_token=next_page_token, action="Order", itemsOrdered={}, order=order)
