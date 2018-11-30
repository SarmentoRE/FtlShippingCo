from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)


def home():
    return render_template("Home.html")


@crud.route("/stock")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    items, next_page_token = get_model().list(cursor=token)

    return render_template(
        "Stocklist.html",
        item=items,
        next_page_token=next_page_token)


@crud.route('stock/<id>')
def view(id):
    item = get_model().read(id)
    return render_template("Stockview.html", item=item)


@crud.route('stock/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        item = get_model().create(data)

        return redirect(url_for('.view', id=item['id']))

    return render_template("Stockform.html", action="Add", item={})


@crud.route('stock/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    item = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        item = get_model().update(data, id)

        return redirect(url_for('.view', id=item['id']))

    return render_template("Stockform.html", action="Edit", item=item)


@crud.route('stock/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
