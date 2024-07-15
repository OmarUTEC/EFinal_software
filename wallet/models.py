from datetime import datetime

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []

def init_db():
    bd = {}
    bd["21345"] = Cuenta("21345", "Arnaldo", 200, ["123", "456"])
    bd["123"] = Cuenta("123", "Luisa", 400, ["456"])
    bd["456"] = Cuenta("456", "Andrea", 300, ["21345"])
    return bd

def get_contacts(db, minumero):
    cuenta = db.get(minumero)
    if not cuenta:
        return {"error": "Cuenta no encontrada"}
    contacts = {contact: db[contact].nombre for contact in cuenta.contactos}
    return contacts

def make_payment(db, minumero, numerodestino, valor):
    cuenta_origen = db.get(minumero)
    cuenta_destino = db.get(numerodestino)
    if not cuenta_origen or not cuenta_destino:
        return {"error": "Cuenta no encontrada"}
    if numerodestino not in cuenta_origen.contactos:
        return {"error": "El destino no es un contacto válido"}
    if cuenta_origen.saldo < valor:
        return {"error": "Saldo insuficiente"}
    cuenta_origen.saldo -= valor
    cuenta_destino.saldo += valor
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cuenta_origen.historial.append(f"Pago realizado de {valor} a {cuenta_destino.nombre} en {timestamp}")
    cuenta_destino.historial.append(f"Pago recibido de {valor} de {cuenta_origen.nombre} en {timestamp}")
    return {"success": f"Pago de {valor} realizado a {cuenta_destino.nombre} en {timestamp}"}

def get_history(db, minumero):
    cuenta = db.get(minumero)
    if not cuenta:
        return {"error": "Cuenta no encontrada"}
    history = {
        "saldo": cuenta.saldo,
        "operaciones": cuenta.historial
    }
    return history
