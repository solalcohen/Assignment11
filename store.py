from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="17011993",
                             db="assignment",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post('/category')
def add_category():
    result = {}
    name_input = request.forms.get('name')
    try:
        with connection.cursor() as cursor:
            sql_previous = 'SELECT name FROM categories'
            cursor.execute(sql_previous)
            entries = cursor.fetchall()
            entries_list = [r['name'] for r in entries]
            if name_input in entries_list:
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'Category already exists'
                result['CAT_ID'] = cursor.lastrowid
                result['CODE'] = 200
            elif name_input == '':
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'Name parameter is missing'
                result['CODE'] = 400
            else:
                sql = "INSERT INTO categories (name) VALUES('{}');".format(name_input)
                cursor.execute(sql)
                connection.commit()
                result['STATUS'] = 'SUCCESS'
                result['MSG'] = 'category created successfully'
                result['CAT_ID'] = cursor.lastrowid
                result['CODE'] = 201
            return json.dumps(result)
    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@delete('/category/<id>')
def delete_category(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT id FROM categories'
            cursor.execute(sql)
            entries = cursor.fetchall()
            entries_list = [r['id'] for r in entries]
            if int(id) not in entries_list:
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'Category not found'
                result['CODE'] = 404
            else:
                sql_delete = "DELETE FROM categories WHERE id={}".format(id)
                cursor.execute(sql_delete)
                connection.commit()
                result['STATUS'] = 'SUCCESS'
                result['CODE'] = 201
            return json.dumps(result)
    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@get('/categories')
def categories():
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT*FROM categories'
            cursor.execute(sql)
            entries = cursor.fetchall()
            connection.commit()
            result['CATEGORIES'] = entries
            result['STATUS'] = 'SUCCESS'
            result['CODE'] = 200
            return json.dumps(result)

    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


# OK CA MARCHE
@post('/product')
def categories():
    result = {}
    category_list = request.forms.get('category')
    title = request.forms.get('title')
    desc = request.forms.get('desc')
    price = request.forms.get('price')
    img_url = request.forms.get('img_url')
    favorite = request.forms.get('favorite')
    id = request.forms.get('id')
    if favorite == 'on':
        real_favorite = True
    else:
        real_favorite = False
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT id FROM product'
            cursor.execute(sql)
            if (category_list is None):
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'category not found'
                result['CODE'] = 404
            elif title == '' or price == '':
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'missing parameters'
                result['CODE'] = 400
            elif id == '':
                sql2 = "INSERT INTO product (title, descr, price, img_url, category, favorite) VALUES ('{0}','{1}',{2},'{3}',{4},{5})".format(
                    title, desc, price, img_url, category_list, real_favorite)
                cursor.execute(sql2)
                connection.commit()
                result['PRODUCT_ID'] = cursor.lastrowid
                result['STATUS'] = 'SUCCESS'
                result['CODE'] = 201
            else:
                sql3 = "UPDATE product SET title='{0}',descr='{1}',price={2},img_url='{3}', category={4},favorite={5} WHERE id={6}".format(
                    title, desc, price, img_url, category_list, real_favorite, id)
                cursor.execute(sql3)
                connection.commit()
                result['PRODUCT_ID'] = cursor.lastrowid
                result['STATUS'] = 'SUCCESS'
                result['CODE'] = 201
            return json.dumps(result)

    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@get('/product/<id>')
def get_product(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'Select id FROM product'
            cursor.execute(sql)
            entries = cursor.fetchall()
            entries_list = [r['id'] for r in entries]
            if id not in entries_list:
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'Product not found'
                result['CODE'] = 404
            else:
                sql_2 = "SELECT*FROM product WHERE id='{}'".format(id)
                cursor.execute(sql_2)
                connection.commit()
                entries = cursor.fetchall()
                result['PRODUCT'] = entries[0]
                result['STATUS'] = 'SUCCESS'
                result['MSG'] = 'SUCCESS'
                result['CODE'] = 200
            return json.dumps(result)
    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@delete('/product/<id>')
def delete_product(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT id FROM product'
            cursor.execute(sql)
            entries = cursor.fetchall()
            entries_list = [r['id'] for r in entries]
            if int(id) not in entries_list:
                result['STATUS'] = 'ERROR'
                result['MSG'] = 'Product not found'
                result['CODE'] = 404
            else:
                sql_delete = "DELETE FROM product WHERE id={}".format(id)
                cursor.execute(sql_delete)
                connection.commit()
                result['STATUS'] = 'SUCCESS'
                result['CODE'] = 201
            return json.dumps(result)
    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@get('/products')
def get_products():
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT*FROM product'
            cursor.execute(sql)
            entries = cursor.fetchall()
            result['PRODUCTS'] = entries
            result['STATUS'] = 'SUCCESS'
            result['CODE'] = 200
            return json.dumps(result)
    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


@get('/category/<id>/products')
def get_listproducts(id):
    result = {}
    cat_prod = []
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT*FROM product'
            cursor.execute(sql)
            entries = cursor.fetchall()
            for dict in entries:
                if dict['category'] == int(id):
                    cat_prod.append(dict)
                    result['PRODUCTS'] = cat_prod
                    result['STATUS'] = 'SUCCESS'
                    result['CODE'] = 200
            return json.dumps(result)

    except:
        result['STATUS'] = 'ERROR'
        result['MSG'] = 'Internal error'
        result['CODE'] = 500
        return json.dumps(result)


run(host='0.0.0.0', port=7000)
