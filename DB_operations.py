import psycopg2
from connect import config
import re

def create_tables():
    command1 = """CREATE TABLE materials (
            name VARCHAR(255) UNIQUE NOT NULL ,
            price INTEGER NOT NULL)"""
    command2 = """ CREATE TABLE products (
                name VARCHAR(255) UNIQUE NOT NULL,
                materials VARCHAR(255) NOT NULL,
                price INTEGER    
                )"""
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute(command1)
        cur.execute(command2)
        
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_material(name, price):
    materialexists = material_exists(name)
    param1 = name
    param2 = price
    sql = """INSERT INTO "materials"(name, price) VALUES(%s, %s)"""
    if materialexists:
        sql = """UPDATE "materials" SET price = %s WHERE name = %s"""
        param1 = price
        param2 = name        
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (param1,param2))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()
            #in case the material is already used in product it's price need's to be updated
            update_db(name)
    return True

def insert_product(name, materials : list):
    price = calculate_price(materials)
    productexists = product_exists(name)
    param1 = name
    param2 = materials
    param3 = price
    sql = """INSERT INTO "products"(name, materials, price) VALUES(%s, %s ,%s)"""
    if productexists: 
        sql = """UPDATE "products" SET  materials = %s, price = %s WHERE name = %s"""
        param1 = materials
        param2 = price
        param3 = name
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (param1,param2,param3))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

        #todo: calculate price
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()
    return True

def product_exists(name): 
    sql = """SELECT * from products where name = %s """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (name,))
        product = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return False
    finally:
        if conn is not None:
            conn.close()
    return len(product) > 0

def material_exists(name): 
    sql = """SELECT * from materials where name = %s """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (name,))
        material = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return False
    finally:
        if conn is not None:
            conn.close()
    return len(material) > 0

def calculate_price(materials : list):
    total_price = 0
    for material_ent in materials:
        material = material_ent.split(',')[0].replace('<', '').replace('>', '')
        amount = material_ent.split(',')[1].replace('<', '').replace('>', '')
        quantity = int(amount) 
        materialprice = material_price(material)
        if(materialprice != None):
            total_price += quantity*int(materialprice)
        else:
            total_price = None
            break
    print(total_price)
    return total_price

def material_price(name):
    material = get_material(name)
    if material != None:
        return material[1]
    return None

def get_material(name):
    sql = """SELECT * from materials where name = %s """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (name,))
        material = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return None
    finally:
        if conn is not None:
            conn.close()
    if len(material) < 1:
        return None
    return (material[0][0],material[0][1])

def get_product(name):
    sql = """SELECT * from products where name = %s """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (name,))
        product = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return None
    finally:
        if conn is not None:
            conn.close()
    if len(product) < 1:
        return None
    return (product[0][1],product[0][2])

def remove_product(name): 
    sql = """DELETE FROM products where name = %s """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (name,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("unable to remove product: ", name)
        print(error)
    finally:
        if conn is not None:
            conn.close()

def remove_material(name):
    sql = """DELETE FROM materials where name = %s """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (name,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("unable to remove material: ", name)
        print(error)
    finally:
        if conn is not None:
            conn.close()

#in case the material is already used in product it's price need's to be updated            
def update_db(material):
    
    sql = """SELECT name, materials from products"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (material,))
        products = cur.fetchall()
        for product in products:
            name = product[0]
            materials = product[1]
            if str(materials).__contains__(material):
                materialsList = re.findall('<.*?>', materials)
                insert_product(name, materialsList)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
