from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from pickle import FALSE
from DB_operations import get_material, get_product, create_tables, insert_material, insert_product, remove_material, remove_product
import re

class requestHandler(BaseHTTPRequestHandler)  :
    def do_GET(self):
        getmaterial = re.search(".*material=", self.path)
        getproduct = re.search(".*product=", self.path,)
        if getmaterial:
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            mat = self.path.split('=')[1]
            mat_value = get_material(mat)
            if mat_value == None: 
                output += '<h1>Value was not found</h1>'
            else:
                output += '<h1>the price of: ' +  mat + ' is: ' + str(mat_value[1]) + '</h1>'

            output += '</body></html>'
            self.wfile.write(output.encode())

        if getproduct:
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            prod = self.path.split('=')[1]
            prod_value = get_product(prod)
            if prod_value == None: 
                output += '<h1>Value was not found</h1>'
            else:
                output += '<h1>the price of: ' +  prod + ' is: ' + str(prod_value[1]) + '</h1>'
            output += '</body></html>'
            self.wfile.write(output.encode())
        

        if self.path.endswith('pricing_server'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<hl>Advanced Pricing Server</hl>'

            output += '<h3>Get Material</h3>'
            output += '<form href = "/pricing_server/material">'
            output += '<input name = "material" type="text"">'
            output += '<input type = submit value="Get">'
            output += '</form>'

            output += '<h3>Get Product</h3>'
            output += '<form>'
            output += '<input type = text name="product">'
            output += '<input type = submit value="Get">'
            output += '</form>'

            output += '<h3>Add\Edit Material</h3>'
            output += '<form method="POST" enctype="multipart/form-data" action="pricing_server/material/new">'
            output += '<input name = "material" type="text" placeholder="e.g. <name, price>">'
            output += '<input type = submit value="Add\Edit">'
            output += '</form>'
            if self.path.__contains__('material_error'): 
                output += '<h4><font color="red">invalid material format</font></h4>'

            output += '<h3>Remove Material</h3>'
            output += '<form method="POST" enctype="multipart/form-data" action="pricing_server/material/remove">'
            output += '<input name = "material" type="text" placeholder="name">'
            output += '<input type = submit value="Remove">'
            output += '</form>'

            output += '<h3>Add\Edit Product</h3>'
            output += '<form method="POST" enctype="multipart/form-data" action="pricing_server/product/new">'
            output += '<input name = "product" type="text" placeholder="e.g. <name, [<material>]>">'
            output += '<input type = submit value="Add\Edit">'
            output += '</form>'
            if self.path.__contains__('product_error'): 
                output += '<h4><font color="red">invalid product format</font></h4>'

            output += '<h3>Remove Product</h3>'
            output += '<form method="POST" enctype="multipart/form-data" action="pricing_server/product/remove">'
            output += '<input name = "product" type="text" placeholder="name">'
            output += '<input type = submit value="Remove">'
            output += '</form>'

            output += '</body></html>'
            self.wfile.write(output.encode())

    def do_POST(self): 
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('content-length'))
        pdict['CONTENT-LENGTH'] = content_len          
        location = '/pricing_server'
        if ctype == 'multipart/form-data':
            if self.path.endswith('/material/new'):
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_material = fields.get('material')[0]
                correct_material = re.search("^<.*,.*>$", new_material)
                if correct_material:
                    material_name = new_material.split(',')[0].replace('<', '').replace('>', '')
                    price = new_material.split(',')[1].replace('<', '').replace('>', '')
                    result = insert_material(material_name, price)
                    if result == False:
                        location = '/material_error' + location
                else:
                    location = '/material_error' + location

            if self.path.endswith('/product/new'):
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_product = fields.get('product')[0]
                correct_product = re.search("^<.*,.*\[<.*>]>$", new_product)
                if correct_product: 
                    product_name = new_product.split(',')[0].replace('<', '').replace('>', '')
                    materials = re.findall("\[.*\]", new_product)[0].replace('[', '').replace(']', '')
                    materials_list = re.findall('<.*?>', materials)
                    result = insert_product(product_name, materials_list)
                    if result == False:
                        location = '/material_error' + location
                else:
                    location = '/product_error' + location
                
            if self.path.endswith('/material/remove'):
                fields = cgi.parse_multipart(self.rfile, pdict)
                name = fields.get('material')[0]
                remove_material(name)

            if self.path.endswith('/product/remove'):
                fields = cgi.parse_multipart(self.rfile, pdict)
                name = fields.get('product')[0]
                remove_product(name)

        self.send_response(301)
        self.send_header('content-type', 'text/html')
        self.send_header('Location', location)
        self.end_headers()

def main():
    create_tables()
    
    PORT = 9000
    server = HTTPServer(("", PORT), requestHandler)
    print("Server running on port %s" % PORT)
    server.serve_forever()

if __name__ == '__main__': 
    main()