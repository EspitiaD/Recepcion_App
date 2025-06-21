from flask import Flask, render_template, request, redirect
from datetime import datetime
import openpyxl
import os

app = Flask(__name__)

def guardar_en_excel(datos):
    archivo = "registro_productos.xlsx"
    existe = os.path.exists(archivo)

    if existe:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Fecha y Hora", "Producto", "Cantidad", "Unidad"])

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for producto, cantidad in datos.items():
        unidad = "unidades" if producto == "Huevos" else "kilos"
        ws.append([ahora, producto, cantidad, unidad])
    
    wb.save(archivo)

@app.route('/')
def productos():
    return render_template("productos.html")

@app.route('/cantidad', methods=['POST'])
def cantidad():
    producto = request.form['producto']
    return render_template("cantidad.html", producto=producto)

@app.route('/resumen', methods=['POST'])
def resumen():
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    return render_template("resumen.html", producto=producto, cantidad=cantidad)

@app.route('/confirmar', methods=['POST'])
def confirmar():
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    guardar_en_excel({producto: cantidad})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
