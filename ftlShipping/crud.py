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
    return render_template("Truckview.html", truck=truck)


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


@crud.route('orders/<id>')
def viewOrders(id):
    order = get_model().readOrder(id)
    return render_template("Orderview.html", order=order)


@crud.route('orders/add', methods=['GET', 'POST'])
def addOrders():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        order = get_model().createOrder(data)

        return redirect(url_for('.view', id=order['id']))

    return render_template("Orderform.html", action="Add", truck={})
# [END add]


@crud.route('orders/<id>/edit', methods=['GET', 'POST'])
def editOrders(id):
    truck = get_model().readOrder(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        truck = get_model().updateOrder(data, id)

        return redirect(url_for('.view', id=truck['id']))

    return render_template("Orderform.html", action="Edit", truck=truck)


@crud.route('orders/<id>/delete')
def deleteOrders(id):
    get_model().deleteOrder(id)
    return redirect(url_for('.listOrders'))


# Begin Stock
@crud.route("/stock")
def listStock():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    items, next_page_token = get_model().listStock(cursor=token)

    return render_template(
        "Stocklist.html",
        item=items,
        next_page_token=next_page_token)


@crud.route('stock/<id>')
def viewStock(id):
    item = get_model().readStock(id)
    return render_template("Stockview.html", item=item)


@crud.route('stock/add', methods=['GET', 'POST'])
def addStock():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        item = get_model().createStock(data)

        return redirect(url_for('.view', id=item['id']))

    return render_template("Stockform.html", action="Add", item={})


@crud.route('stock/<id>/edit', methods=['GET', 'POST'])
def editStock(id):
    item = get_model().readStock(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        item = get_model().updateStock(data, id)

        return redirect(url_for('.view', id=item['id']))

    return render_template("Stockform.html", action="Edit", item=item)


@crud.route('stock/<id>/delete')
def deleteStock(id):
    get_model().deleteStock(id)
    return redirect(url_for('.listStock'))
