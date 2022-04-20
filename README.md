# PolyrizeTest

this is an advanced Webserver built in python. 
D:\python\PolyrizeTest\screen shots\advanced web server.PNG
![web server](/screen_shots/advanced_web_server.PNG?raw=true "Advance Web Server")

the server is hosted under: 
http://localhost:9000/pricing_server

the server uses postgresql DB to store data. the DB connection details can be found in the database.ini file please edit this file to fit your db details. 

the server allows getting the value of a stored material: 
http://localhost:9000/pricing_server?material=material_name
in case the values is not found a 'Value was not found' message will be displayed


the server allows getting the value of a stored product: 
http://localhost:9000/pricing_server?product=product_name
in case the values is not found a 'Value was not found' message will be displayed

the server allows you to add\Edit materials: 
	the Add\Edit button uses multi-part form to parse your request and add the value to the db. 
	the material added should follow the following convention: 
	'<material_name, material_price>'
	when adding a new material or editting an existing one the server will check all the products that use this material and updates it price accordingly (see product below)
	an error message will be displayed in case the adding the material is not successfull (incorrect format, ...)
	
the server allows you to add\Edit products: 
	the Add\Edit button uses multi-part form to parse your request and add the value to the db. 
	the product added should follow the following convention: 
	'<product_name, [<material1_name, quantity1>, <material2_name, quantity2>, ...]>'
	when adding a new product the server will try to calculate it's price based on it's materials in case it doesn't succeed (material not foun, ..) it will write NULL instead
	an error message will be displayed in case the adding the product is not successfull (incorrect format, ...)
	
the server allows to Remove product and material: 
	based on the name given the server will delete the product\material in case it exists. 
	no error message will be displayed in case the name doesn't exist. 


in order to run the server please use the pricing_webserver.py file.