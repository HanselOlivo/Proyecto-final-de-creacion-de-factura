from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_mysqldb import MySQL,MySQLdb 
import os
from datetime import datetime, timedelta
import pdfkit
import smtplib
from email.message import EmailMessage

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] =  'static/uploads'

pdf_output_folder = r'C:\Users\xLekh\Desktop\logg proct\static\pdfs'

wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    return render_template('home.html')


@app.route('/admin_menu')
def admin_menu():
    return render_template('adminhome.html')

@app.route('/user_menu')
def user_menu():
    return render_template('usermenu.html')


@app.route('/user')
def user():
    return render_template('home2.html')  


@app.route('/login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST':
       
        correo = request.form['txtCorreo']
        password = request.form['password']
        
        print(correo, password)

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (correo, password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            
            if session['id_rol']==1:
                return redirect(url_for('admin_menu'))
            elif session['id_rol']==2:
                return render_template("usermenu.html")
        else:
            return render_template('index.html')
        
    return render_template('index.html')
        
 #-----------------register-------------------------------------------------------------------#

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/crete-register', methods = ["GET","POST"])
def create_register():
    correo=request.form['txtCorreo']
    password = request.form['password']


    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '2')", (correo, password))
    mysql.connection.commit()

    return redirect(url_for('login'))
      



#-------------------list user------------------------------------------------------------------#



@app.route("/listar", methods= ["GET", "POST"])
def listar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE  id_rol='2'")
    usuarios = cur.fetchall()
    cur.close()
    
    return render_template("User_list.html", usuarios=usuarios)


@app.route('/eliminar_user/<int:id>')
def eliminar_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()

    return redirect(url_for('listar'))


#-------------------list Admin------------------------------------------------------------------#



@app.route("/listar_adm", methods= ["GET", "POST"])
def listar_adm():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE  id_rol='1'")
    admin = cur.fetchall()
    cur.close()
    
    return render_template("admin_list.html", admin=admin)

#----------------------------inventory-----------------------------------------#

@app.route('/inventario', methods = ['GET', 'DELETE'])
def inventario():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventario')
    data = cursor.fetchall()
    cursor.close()
    return render_template('inventario.html', datos=data)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventario WHERE descripcion LIKE %s", ('%' + query + '%',))
    results = cur.fetchall()
    cur.close()
    
    print(results)
    return jsonify(results)

@app.route('/obtener_datos_inv')
def  obtener_datos_inv():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventario')
    data = cursor.fetchall()
    cursor.close()
    return data

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        art_name = request.form['art_name']
        art_price = request.form['art_precio']
        art_itbis = request.form['art_itbis']
        art_cant = request.form['art_cantidad']
        art_img = request.files['image']

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM inventario WHERE descripcion = %s", (art_name,))
        existing_article = cur.fetchone()

        if existing_article:
            flash('El artículo ya existe en la base de datos', 'error')
            return redirect(url_for('inventario'))
        
        if art_img.filename != '':
            art_img.save(os.path.join(app.config['UPLOAD_FOLDER'], art_img.filename))


        cur.execute("INSERT INTO inventario (descripcion, precio, cantidad, itbis, img, cantidad_a) VALUES (%s,%s,%s,%s,%s,%s)", (art_name, art_price, art_cant, art_itbis, art_img.filename, art_cant))
        mysql.connection.commit()
        cur.close()
        
    return redirect(url_for('inventario'))

@app.route('/remove_art/<string:id>', methods=['DELETE'])
def remove_art(id):

    if request.method == 'DELETE':

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM inventario WHERE id = {0}'.format(id))
        mysql.connection.commit()
        flash('Contact Removed Successfully')
        return redirect(url_for('inventario'))

@app.route('/edit/<id>')
def get_art(id):
    cur = mysql.connection.cursor()
    cur.execute(' SELECT * FROM inventario WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_inv.html',datos = data[0])

@app.route('/update/<id>', methods = ['POST', 'GET'])
def update(id):

    if request.method == 'POST':

        art_name = request.form['art_name']
        art_price = request.form['art_precio']
        art_itbis = request.form['art_itbis']
        art_cant = request.form['art_cantidad']
        art_imagen = request.files['image']

        if art_imagen.filename != '':
            art_imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], art_imagen.filename))
        elif art_imagen.filename == '':
            cur = mysql.connection.cursor()
            cur.execute('SELECT img FROM inventario WHERE id = %s',(id,))
            art_imagen.filename = cur.fetchone()

        cur = mysql.connection.cursor()
        cur.execute('UPDATE inventario SET descripcion = %s, precio = %s, cantidad = %s, itbis = %s, img = %s, cantidad_a = cantidad WHERE id = %s', (art_name, art_price, art_cant, art_itbis, art_imagen.filename,id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('inventario'))
    
#----------------------------Facturas-----------------------------------------#


# Manejador de error para URL no encontrada (404)

@app.errorhandler(404)
def page_not_found(error):
    previous_page = request.referrer
    if previous_page is None:
        return redirect(url_for('index'))
    return redirect(previous_page)

#~ enviar facturas
def enviar(id):
    pdf_output_path = os.path.join(pdf_output_folder, 'factura.pdf')
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    id_factura = str(id)
    session['id_factura_enviada'] = int(id_factura)

    # Renderiza el contenido HTML
    url = 'http://127.0.0.1:5000/factura_detalle/' + id_factura

    # Genera el PDF desde el HTML
    pdf = pdfkit.from_url(url, False, configuration=config)

    # Guarda el PDF como archivo en la carpeta especificada
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf)

    enviar_e()

    # Devuelve una respuesta con la ubicación del archivo PDF generado
    return f'PDF generado y guardado en: {pdf_output_path}'

@app.route('/enviar_Email')
def enviar_e():

    pdf_output_path = os.path.join(pdf_output_folder, 'factura.pdf')
    pdf_path = pdf_output_path

    # Configuración del correo electrónico
    correo_remitente = "tecknopoint1@gmail.com"
    contrasena_remitente = "mrvw gpsb whcr tjjx"
    correo_destinatario = "slimerbatista27@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    # Crear mensaje de correo electrónico
    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "Factura adjunta"
    email.set_content("Adjunto encontrarás la factura")

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)

    # Send Customer

    id_factura = session['id_factura_enviada']

    cur = mysql.connection.cursor()
    cur.execute("SELECT customer FROM bills WHERE id = %s", (id_factura,))
    customer = cur.fetchone()
    
    print(customer)

    cur.execute("SELECT client_email FROM clients WHERE client_name = %s", (customer['customer'],))
    email_client = cur.fetchone()['client_email']
    
    print(email_client)

    correo_remitente = "tecknopoint1@gmail.com"
    contrasena_remitente = "mrvw gpsb whcr tjjx"
    correo_destinatario = email_client
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = "Factura adjunta"
    email.set_content("Adjunto encontrarás la factura")

    with open(pdf_path, "rb") as attachment:
        contenido_pdf = attachment.read()
    email.add_attachment(contenido_pdf, maintype="application", subtype="octet-stream", filename=os.path.basename(pdf_path))

    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)
        smtp.send_message(email)


    return redirect(url_for('article'))

@app.route('/factura/<id>')
def factura(id):
    
    session['id_factura'] = id

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE id = %s",(id,))
    bill = cur.fetchall()
    cur.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM art_bill WHERE id_bills = %s",(id,))
    detail = cursor.fetchall()
    cursor.close()

    total_general = 0
    sub_total = 0
    total_itbis = 0
    fecha_N = 0

    for fila in detail:
        art_price = fila['price']
        art_itbis = fila['itbis']
        art_mount = fila['amount']

        subtotal = art_mount * art_price
        itbis = subtotal + ( subtotal * art_itbis / 100)
        sub_itbis = subtotal * art_itbis / 100

        # Calcular el total general sumando subtotal e ITBIS de cada producto
        total_general += itbis
        sub_total += art_mount * art_price
        total_itbis += sub_itbis
    
    # Formatear los números total_general e itbis con dos decimales
    total_general_formatted = "{:.2f}".format(total_general)
    sub_total_formatted = "{:.2f}".format(sub_total)
    total_itbis_formatted = "{:.2f}".format(total_itbis)
    
    for fila in bill:
        fecha_N = fila['date']

    fecha_V = fecha_N + timedelta(days=30)

    return render_template("factura.html", bill=bill, detail=detail, total_itbis = total_itbis_formatted, subtotal = sub_total_formatted, total_general=total_general_formatted, fecha = fecha_V)

#~ PDF
@app.route('/descargar_pdf')
def descargar_pdf():

    id_factura = session['id_factura']

    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/factura/' + id_factura
    
    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    id_factura_int = int(id_factura)
    
    if id_factura_int >= 10:
        # Crea una respuesta para descargar el PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=factura N. 000' + id_factura + '.pdf'
    elif id_factura_int > 99:
        # Crea una respuesta para descargar el PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=factura N. 00' + id_factura + '.pdf'
    else:
        # Crea una respuesta para descargar el PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=factura N. 0000' + id_factura + '.pdf'

    return response

@app.route('/descargar_cotizacion_pdf')
def descargar_cotizacion_pdf():

    id_cotizacion = session['id_cotizacion']

    # URL del contenido a convertir en PDF
    url = 'http://127.0.0.1:5000/cotizacion_p/' + id_cotizacion
    
    # Genera el PDF desde la URL
    pdf = pdfkit.from_url(url, False, configuration=config)

    id_cotizacion_int = int(id_cotizacion)
    
    if id_cotizacion_int >= 10:
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=cotizacion N. 000' + id_cotizacion + '.pdf'
    elif id_cotizacion_int > 99:
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=cotizacion N. 00' + id_cotizacion + '.pdf'
    else:
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=cotizacion N. 0000' + id_cotizacion + '.pdf'

    return response


#? Pago con Tarjeta
@app.route('/pay', methods=["GET","POST"])
def pay():

    IA()

    # Obtener los datos del formulario
    numero_tarjeta = request.form['numero_tarjeta']
    nombre_titular = request.form['nombre_titular']
    fecha_vencimiento = request.form['fecha_vencimiento']
    cvv = request.form['cvv']
    discount = request.form['discount']
    ex_itbis = request.form['ex-itbis']
    cliente = request.form['cliente']
    cajero = request.form['cajero']
    total = request.form['total']

    # Obtener los datos del cliente
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM clients WHERE client_id=%s"
    data = (cliente,)
    cursor.execute(query, data)
    result = cursor.fetchone()

    rnc = result['rnc_client']
    ubicacion = result['client_address']
    contacto = result['client_phone']
    customer = result['client_name']

    # Total
    partes = total.split()
    numero = partes[1]
    total_sin_dolar = numero.strip('$')
    total_general = str(total_sin_dolar)

    # Verificar si el número de tarjeta es válido o no
    # tarjeta = CreditCard(numero_tarjeta)
    tarjeta = numero_tarjeta

    new_id = CIB()

    if tarjeta:
        fecha_hora = datetime.now()
        fecha_hora_formateada = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")

        number_bill = GNF()

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO bills (id, date, number_bill, customer, discount, way_to_pay, paid,`change`, cashier, rnc_client_bill, ubicacion, contacto, total_general, estado, Itbisextra) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (new_id, fecha_hora_formateada, number_bill, customer, discount, "Tarjeta", "0", "0", cajero, rnc, ubicacion, contacto, total_general, 1, ex_itbis))
        mysql.connection.commit()
        APB(new_id)

        enviar(new_id)

        cur.execute("DELETE FROM articulos")
        mysql.connection.commit()
        cur.close()

        flash("La compra se realizó con éxito")
        return redirect(url_for('article'))
    else:
        flash("Hubo un problema con la tarjeta")
        return redirect(url_for('article'))

def APB(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articulos")

    # Obtener todas las filas de la consulta como una lista de tuplas
    articulos = cur.fetchall()

    for articulo in articulos:
        # Insertar cada campo en la tabla art_bills
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO art_bill (id_bills, decrition, price, itbis, amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (id, articulo['descripcion'], articulo['precio'], articulo['itbis'], articulo['cantidad']))

        # (Optional) Commit the changes to the database
        mysql.connection.commit()

def CIB():
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT MAX(id) FROM bills")

    resultado = cur.fetchone()
    
    print(resultado)

    if resultado is None or resultado['MAX(id)'] is None:
        next_bill = 1
    else:
        next_bill = resultado['MAX(id)'] + 1
    cur.close()

    return next_bill
    
def GNF():
    last_number_bill = OUNFD()

    if not last_number_bill:
        new_number_bill = '00001'
    else:
       
        new_number = int(last_number_bill) + 1
        
        new_number_bill = '{:05d}'.format(new_number)

    return new_number_bill


def OUNFD():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT number_bill FROM bills ORDER BY number_bill DESC LIMIT 1")
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return resultado['number_bill']
        else:
            return None
    except mysql.connector.Error as e:
        print("Error al obtener el último número de factura:", e)
        return None
    
def IA():
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT * FROM articulos")
        articles = cur.fetchall()

        for article in articles:
            id_articles = article['id']

            cur.execute("SELECT cantidad FROM inventario WHERE id = %s", (id_articles,))
            amount = cur.fetchone()

            cur.execute("UPDATE inventario SET cantidad_a = %s WHERE id = %s", (amount, id_articles))

    finally:
        cur.close()

#* Pago con Efectivo
@app.route("/payment", methods=["GET", "POST"])
def payment():
    
    IAE()

    # Obtener los datos del formulario
    cliente = request.form['cliente']
    cajero = request.form['cajero']
    monto = request.form['monto']
    total = request.form['total']
    discount = request.form['discount']
    ex_itbis = request.form['ex-itbis']

    # Obtener los datos del cliente
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM clients WHERE client_id=%s"
    data = (cliente,)
    cursor.execute(query, data)
    result = cursor.fetchone()

    rnc = result['rnc_client']
    ubicacion = result['client_address']
    contacto = result['client_phone']
    customer = result['client_name']

    # Total
    partes = total.split()
    numero = partes[1]
    total_sin_dolar = numero.strip('$')
    total_general = str(total_sin_dolar)

    total_float = float(total_general)
    monto_float = float(monto)

    cambio = monto_float - total_float

    new_id = CIBE()

    fecha_hora = datetime.now()
    fecha_hora_formateada = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")

    number_bill = GNFE()

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO bills (id, date, number_bill, customer, discount, way_to_pay, paid, `change`, cashier, rnc_client_bill, ubicacion, contacto, total_general, estado, Itbisextra) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (new_id, fecha_hora_formateada, number_bill, customer, discount, "Efectivo", monto_float, cambio, cajero, rnc, ubicacion, contacto, total_general, 1, ex_itbis))
    mysql.connection.commit()
    APBE(new_id)

    enviar(new_id)

    cur.execute("DELETE FROM articulos")
    mysql.connection.commit()
    cur.close()

    flash("La compra se realizó con éxito")
    return redirect(url_for('article'))

def APBE(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articulos")

    # Obtener todas las filas de la consulta como una lista de tuplas
    articulos = cur.fetchall()

    for articulo in articulos:
        # Insertar cada campo en la tabla art_bills
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO art_bill (id_bills, decrition, price, itbis, amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (id, articulo['descripcion'], articulo['precio'], articulo['itbis'], articulo['cantidad']))

        # (Optional) Commit the changes to the database
        mysql.connection.commit()

def CIBE():
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT MAX(id) FROM bills")

    resultado = cur.fetchone()
    
    print(resultado)

    if resultado is None or resultado['MAX(id)'] is None:
        next_bill = 1
    else:
        next_bill = resultado['MAX(id)'] + 1
    cur.close()

    return next_bill
    
def GNFE():
    last_number_bill = OUNFDE()

    if not last_number_bill:
        new_number_bill = '00001'
    else:
       
        new_number = int(last_number_bill) + 1
        
        new_number_bill = '{:05d}'.format(new_number)

    return new_number_bill


def OUNFDE():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT number_bill FROM bills ORDER BY number_bill DESC LIMIT 1")
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return resultado['number_bill']
        else:
            return None
    except mysql.connector.Error as e:
        print("Error al obtener el último número de factura:", e)
        return None
    
def IAE():
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT * FROM articulos")
        articles = cur.fetchall()

        for article in articles:
            id_articles = article['id']

            cur.execute("SELECT cantidad FROM inventario WHERE id = %s", (id_articles,))
            amount = cur.fetchone()

            cur.execute("UPDATE inventario SET cantidad_a = %s WHERE id = %s", (amount, id_articles))

    finally:
        cur.close()

#! Search
@app.route('/buscar', methods=['POST'])
def buscar():
    query = request.form['query']
    resultados = buscar_en_bd(query)
    return jsonify(resultados)

def buscar_en_bd(query):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT product_name FROM products WHERE product_name LIKE %s", ('%' + query + '%',))
    resultados = [row[1] for row in cursor.fetchall()]
    cursor.close()
    return resultados

#* Bills
@app.route('/bills', methods=['GET','POST'])
def bill():
    bills = obtener_bills()
    return render_template('bills.html', bills = bills)

@app.route('/bills_table')
def obtener_bills():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE estado = %s",("1"))
    data = cur.fetchall()
    cur.close()

    return data

@app.route('/factura_detalle/<id>')
def factura_detalle(id):

    session['id_factura'] = id

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE id = %s",(id,))
    bill = cur.fetchall()
    cur.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM art_bill WHERE id_bills = %s",(id,))
    detail = cursor.fetchall()
    cursor.close()

    total_general = 0
    sub_total = 0
    total_itbis = 0
    total_discount = 0
    total_ex_itbis = 0

    for fila in detail:
        art_price = fila['price']
        art_itbis = fila['itbis']
        art_mount = fila['amount']

        subtotal = art_mount * art_price
        itbis = subtotal + ( subtotal * art_itbis / 100)
        sub_itbis = subtotal * art_itbis / 100

        # Calcular el total general sumando subtotal e ITBIS de cada producto
        total_general += itbis
        sub_total += art_mount * art_price
        total_itbis += sub_itbis

        for fila1 in bill:

            discount = fila1['discount']
            ex_itbis = fila1['Itbisextra']

            total_discount += subtotal * discount / 100
            total_ex_itbis += sub_total * ex_itbis / 100
        
    total_general_discount = total_general - total_discount
    total_general_ex_itbis = total_general_discount + total_ex_itbis
    
    # Formatear los números total_general e itbis con dos decimales
    total_general_formatted = "{:.2f}".format(total_general_ex_itbis)
    sub_total_formatted = "{:.2f}".format(sub_total)
    total_itbis_formatted = "{:.2f}".format(total_itbis)
    
    for fila in bill:
        fecha_N = fila['date']

    fecha_V = fecha_N + timedelta(days=30)

    return render_template("detalle.html", bill=bill, detail=detail, total_itbis = total_itbis_formatted, subtotal = sub_total_formatted, total_general=total_general_formatted, fecha = fecha_V)

#TODO Customers
@app.route('/obtener_customer')
def obtener_customer():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clients WHERE activity_id = %s",("1"))
    client = cursor.fetchall()
    cursor.close()

    return client

#------------------------------Articles-----------------------------------------------------------------------
@app.route('/article')
def article():
    datos = obtener_datos_inv()
    articles = obtener_articles()
    calculo = calculos()
    customer = obtener_customer()
    return render_template('articles.html', datos = datos, articles = articles, calculo = calculo, customer = customer, fullname = "Hansel")

@app.route('/calculos')
def calculos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT precio, itbis, cantidad FROM articulos')
    cal = cur.fetchall()

    resultados = []

    total_price = 0
    total_itbis = 0

    for fila in cal:
        art_price = fila['precio']
        art_itbis = fila['itbis']
        art_mount = fila['cantidad']

        subtotal = art_mount * art_price
        
        if art_itbis == art_itbis:
            itbis = art_itbis
        else:
            itbis += art_itbis

        subtotal_itbis = itbis * subtotal / 100

        total_price += subtotal
        total_itbis += subtotal_itbis

    # Calculate total as the sum of subtotal and ITBIS
    total_total = total_price + total_itbis

    # Redondear los valores a dos decimales
    total_price = round(total_price, 2)
    total_itbis = round(total_itbis, 2)
    total_total = round(total_total, 2)

    resultados.append({'subtotal': total_price, 'itbis': total_itbis, 'total': total_total})

    return resultados

@app.route('/obtener_articles')
def obtener_articles():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM articulos')
    article = cursor.fetchall()
    cursor.close()
    return article

@app.route('/incluir_art/<int:id>')
def incluir(id):
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM inventario WHERE id = %s', (id,))
    data = cur.fetchone()

    if not data:
        flash('El artículo no existe en el inventario.')
    else:
        art_id = data['id']
        art_name = data['descripcion']
        art_price = data['precio']
        art_itbis = data['itbis']
        art_mount = 1

        cur.execute('INSERT INTO articulos (id, descripcion, precio, itbis, cantidad) VALUES (%s, %s, %s, %s, %s)', (art_id, art_name, art_price, art_itbis, art_mount))
        mysql.connection.commit()

        cur.execute('UPDATE inventario SET cantidad = cantidad - 1 WHERE id = %s', (id,))
        mysql.connection.commit()

        cur.close()
        return redirect(url_for('article'))
    
    return redirect(url_for('article'))


def enviar_alerta(producto,amount):

    nombre_p = producto
    stock = amount

    # Enviar correo electronico cuando se logue e usuario
    correo_remitente = "tecknopoint1@gmail.com"
    contrasena_remitente = "mrvw gpsb whcr tjjx"
    correo_destinatario = "slimerbatista27@gmail.com"
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587

    correo_destinatario = email
    asunto="¡Alerta de Stock Bajo! 🚨"
    mensaje=f"""
                Solo quería advertirte que nuestro stock de {nombre_p} está llegando a niveles críticos. Actualmente solo quedan {stock} unidades disponibles en el punto de venta.

                ¡Es hora de reabastecer antes de que sea demasiado tarde!

                Gracias,
                TecknoPoint"""

    email = EmailMessage()
    email["From"] = correo_remitente
    email["To"] = correo_destinatario
    email["Subject"] = asunto
    email.set_content(mensaje)

    with smtplib.SMTP(servidor_smtp, puerto_smtp) as smtp:
        smtp.starttls()
        smtp.login(correo_remitente, contrasena_remitente)

        smtp.send_message(email)

@app.route('/agregar_cantidad_art/<int:id>')
def agregar_cantidad(id):
    try:
        cur = mysql.connection.cursor()

        session['id_product'] = id
        
        print("id del articulo: ",id)

        # Obtener la cantidad actual del artículo
        cur.execute('SELECT cantidad FROM articulos WHERE id = %s', (id,))
        result_current = cur.fetchone()
        
        print("cantidad articulos: ",result_current)

        if result_current:
            current_quantity = result_current['cantidad']  # Acceder al primer elemento de la tupla
        else:
            flash('No se encontró ningún artículo con el ID especificado.')
            return redirect(url_for('article'))

        # Obtener la cantidad límite del producto asociado al artículo
        cur.execute('SELECT cantidad_a FROM inventario WHERE id = %s', (id,))
        result_limit = cur.fetchone()

        print("cantidad actual en inventario: ", result_limit)
        
        if result_limit:
            limit_quantity = result_limit['cantidad_a']  # Acceder al primer elemento de la tupla
        else:
            flash('No se encontró ninguna cantidad límite para el artículo con el ID especificado.')
            return redirect(url_for('article'))

        print("Cantidad actual del artículo:", current_quantity)
        print("Cantidad límite del producto:", limit_quantity)

        # Verificar si la cantidad actual supera la cantidad límite
        if current_quantity >= limit_quantity:
            flash('No se puede agregar más cantidad. Límite alcanzado.')
            print('Estoy aquí, mensaje es para ti')
        else:
            # Incrementar la cantidad del artículo
            cur.execute('UPDATE articulos SET cantidad = cantidad + 1 WHERE id = %s', (id,))
            mysql.connection.commit()

            cur.execute('UPDATE inventario SET cantidad = cantidad - 1 WHERE id = %s', (id,))
            mysql.connection.commit()
            flash('Cantidad agregada correctamente.')
    except Exception as e:
        flash('Error al agregar cantidad: {}'.format(str(e)))
    finally:
        cur.close()

    return redirect(url_for('article'))

@app.route('/quitar_cantidad_art/<id>')
def quitar_cantidad(id):
    cur = mysql.connection.cursor()
    
    # Obtener la cantidad actual del producto en la tabla articulos
    cur.execute('SELECT cantidad FROM articulos WHERE id = %s', (id,))
    result = cur.fetchone()

    if result is not None:  # Verificar si la consulta devolvió un resultado
        current_quantity = result['cantidad']  # Acceder al valor de la clave 'cantidad'

        # Verificar si la cantidad es mayor que cero antes de restar
        if current_quantity > 1:
            cur.execute('UPDATE inventario SET cantidad = cantidad + 1 WHERE id = %s', (id,))
            mysql.connection.commit()

            # Decrementar la cantidad solo si es mayor que cero
            cur.execute('UPDATE articulos SET cantidad = cantidad - 1 WHERE id = %s', (id,))
            mysql.connection.commit()
        else:
            flash('La cantidad no puede ser menor que cero.')
    else:
        flash('No se encontró ningún artículo con el ID especificado.')

    cur.close()
    return redirect(url_for('article'))

@app.route('/remove_article/<string:id>')
def remove_article(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM articulos WHERE id = {0}'.format(id))
    mysql.connection.commit()

    cur.execute('UPDATE inventario SET cantidad = cantidad + 1 WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('article'))

#* Cotizacion
@app.route('/cotizacion')
def cotizacion():
    cotiz = obtener_cotizacion()
    return render_template('cotizacion.html', cotiz = cotiz)

@app.route('/cotizacion_table')
def obtener_cotizacion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE estado = %s",("1"))
    data = cur.fetchall()
    cur.close()

    return data

@app.route('/detalle_cotizacion/<id>')
def detalle_cotizacion(id):

    session['id_cotizacion'] = id

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE id = %s",(id,))
    bill = cur.fetchall()
    cur.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM art_bill WHERE id_bills = %s",(id,))
    detail = cursor.fetchall()
    cursor.close()

    total_general = 0
    sub_total = 0
    total_itbis = 0
    total_discount = 0
    total_ex_itbis = 0

    for fila in detail:
        art_price = fila[3]
        art_itbis = fila[4]
        art_mount = fila[5]

        subtotal = art_mount * art_price
        itbis = subtotal + ( subtotal * art_itbis / 100)
        sub_itbis = subtotal * art_itbis / 100

        # Calcular el total general sumando subtotal e ITBIS de cada producto
        total_general += itbis
        sub_total += art_mount * art_price
        total_itbis += sub_itbis
    
        for fila1 in bill:
            discount = fila1[4]
            ex_itbis = fila1[14]

            total_discount += subtotal * discount / 100
            total_ex_itbis += sub_total * ex_itbis / 100
        
    total_general_discount = total_general - total_discount
    total_general_ex_itbis = total_general_discount + total_ex_itbis

    # Formatear los números total_general e itbis con dos decimales
    total_general_formatted = "{:.2f}".format(total_general_ex_itbis)
    sub_total_formatted = "{:.2f}".format(sub_total)
    total_itbis_formatted = "{:.2f}".format(total_itbis)
    
    for fila in bill:
        fecha_N = fila[1]

    fecha_V = fecha_N + timedelta(days=30)

    return render_template("detalle_cotizacion.html", bill=bill, detail=detail, total_itbis = total_itbis_formatted, subtotal = sub_total_formatted, total_general=total_general_formatted, fecha = fecha_V)

#? Empleados Funcion
@app.route('/obtener_datos_emp')
def  obtener_datos_emp():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE role_id = %s",('3'))
    data = cursor.fetchall()
    cursor.close()
    return data 

#& Logout
@app.route('/logout')
def logout():

    session.clear()
    mensage = 'Sesión cerrada exitosamente', 'success'

    return redirect(url_for('home'))

if __name__ == '__main__':
   app.secret_key = "pinchellave"
   app.run(debug=True)