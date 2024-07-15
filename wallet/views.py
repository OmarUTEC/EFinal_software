from flask import request, jsonify
from wallet import app
from wallet.models import init_db, get_contacts, make_payment, get_history

# Inicializar la base de datos con cuentas y contactos
db = init_db()

@app.route('/billetera/contactos', methods=['GET'])
def contactos():
    minumero = request.args.get('minumero')
    contacts = get_contacts(db, minumero)
    return jsonify(contacts)

@app.route('/billetera/pagar', methods=['POST'])
def pagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))
    result = make_payment(db, minumero, numerodestino, valor)
    return jsonify(result)

@app.route('/billetera/historial', methods=['GET'])
def historial():
    minumero = request.args.get('minumero')
    history = get_history(db, minumero)
    return jsonify(history)
