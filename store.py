from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='bensql',
    db='ben_online_store',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

@get("/admin")
def admin_portal():
    print "in admin"
    return template("pages/admin.html")



@get("/")
def index():
    print "in index"
    return template("index.html")


@get("/categories")
def get_category_list():
    print "in get category"
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM catagory'
            cursor.execute(sql)
            categories = cursor.fetchall()
            status = "sucess"
            code = '200 -success'
            msg = ""
            connection.commit()
    except Exception as e:
        status = "error"
        msg = repr(e)
        code = '500 - internal error'

    result = {"STATUS": status, "CATEGORIES": categories, "MSG":msg, "CODE":code}
    return json.dumps(result)


@post("/category")
def create_category():
    category_name = request.POST.get('name')
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO catagory (name) VALUES ("{}")'.format(category_name)
            cursor.execute(sql)
            cat_id = cursor.lastrowid
            connection.commit()
            status = "success"
            msg=""
            print "success code category created - 201"

    except Exception as e:
        status = "error"
        msg = repr(e)
        cat_id=0
    result = {"STATUS": status, "CAT_ID": cat_id, "MSG": msg}
    return json.dumps(result)


@get("/product/<product_id>")
def get_a_product(product_id):
    print "inside get a product"
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product WHERE id=("{}")'.format(product_id)
            cursor.execute(sql)
            product = cursor.fetchall()
            connection.commit()
            status = "success"
            msg= ""
            print "success code - 200"

    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg, "PRODUCT": product}
    return json.dumps(result)


@get("/category/<category_id>/products")
def get_products_by_category(category_id):
    print "inside category products"
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product WHERE category= ("{}")'.format(category_id)
            cursor.execute(sql)
            products = cursor.fetchall()
            connection.commit()
            status = "success"
            msg= ""
            print "success code - 200"

    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg, "PRODUCTS": products}
    return json.dumps(result)


@get("/products")
def get_all_products():
    print "inside get all products"
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product'
            cursor.execute(sql)
            products = cursor.fetchall()
            connection.commit()
            status = "success"
            msg= ""
            print "success code - 200"

    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg, "PRODUCTS": products}
    return json.dumps(result)


@post("/product")
def add_or_update_product(title,desc,price,img_url,category,favorite,id=0):

        try:
            with connection.cursor() as cursor:
                if id == 0:
                    sql = 'INSERT INTO product (title,desc,price,img_url,category,favorite) ' \
                          'VALUES ("{0}","{1}","{2}","{3}","{4}","{5}")'.format(category,desc,price,title,favorite,img_url)
                elif id>0 :
                    sql = 'UPDATE product SET category="{0}", description="{1}", price="{2}", title="{3}",favorite="{4}"' \
                          ',img_url="{5}" WHERE id="{6}"'.format(category,desc,price,title,favorite,img_url,id)
                cursor.execute(sql)
                product_id = id
                connection.commit()
                status = "success"
                msg = ""
                print "success code - 201 product create/updated"

        except Exception as e:
            status = "error"
            msg = repr(e)

        result = {"STATUS": status, "MSG": msg, "PRODUCT_ID": product_id}
        return json.dumps(result)



@delete("/category/<del_this_category_id>")
def delete_category(del_this_category_id):
    print "inside delete category"
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM catagory WHERE id= ("{}")'.format(del_this_category_id)
            cursor.execute(sql)
            connection.commit()
            status = "success"
            msg = ""
            print "success code - 201 category deleted"
    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg}
    return json.dumps(result)


@delete("/product/<del_this_product_id>")
def delete_product(del_this_product_id):
    print "inside delete product"
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM product WHERE id= ("{}")'.format(del_this_product_id)
            cursor.execute(sql)
            connection.commit()
            status = "success"
            msg = ""
            print "success code - 201 category deleted"
    except Exception as e:
        status = "error"
        msg = repr(e)

    result = {"STATUS": status, "MSG": msg}
    return json.dumps(result)

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=7008)

if __name__ == '__main__':
    main()
