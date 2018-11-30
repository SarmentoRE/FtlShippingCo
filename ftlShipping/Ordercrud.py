from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)


def home():
    return render_template("Home.html")


@crud.route("/orders")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    trucks, next_page_token = get_model().list(cursor=token)

    return render_template(
        "Orderlist.html",
        truck=trucks,
        next_page_token=next_page_token)


@crud.route('orders/<id>')
def view(id):
    truck = get_model().read(id)
    return render_template("Orderview.html", truck=truck)


@crud.route('orders/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        truck = get_model().create(data)

        return redirect(url_for('.view', id=truck['id']))

    return render_template("Orderform.html", action="Add", truck={})
# [END add]


@crud.route('orders/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    truck = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        truck = get_model().update(data, id)

        return redirect(url_for('.view', id=truck['id']))

    return render_template("Orderform.html", action="Edit", truck=truck)


@crud.route('orders/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))