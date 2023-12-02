import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

conn = sqlite3.connect("dispositivo.db")
c = conn.cursor()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080", 
                   "http://localhost:8000", 
                   "https://iot-backen-5cc85ad97e0a.herokuapp.com", 
                   "https://iotfront-b4cb0f781573.herokuapp.com"],
    allow_credentials=True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

class Dispositivo(BaseModel):
    nombre : str
    valor: str

@app.get('/')
def root():
    return {"Bienvenido a la API REST"}

@app.get("/dispositivo")
async def mostrar_dispositivo():
    """Obtiene todos los dispositivos"""
    c.execute('SELECT * FROM dispositivo')
    response=[{"id": row[0], "nombre": row[1], "valor": row[2]} for row in c.fetchall()]
    return response 
@app.get("/led/{id}")
async def obtener_led(id: str):
    """Obtiene un valor"""
    c.execute('SELECT * FROM dispositivo WHERE id = ?', (id,))
    row = c.fetchone()
    if row:
        dispositivo = {"id": row[0], "nombre": row[1], "valor": row[2]}
        return dispositivo
    else:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

@app.put("/potenciometro/{id}")
async def actualizar_dispositivo(id: str, dispositivo: Dispositivo):
    """Actualiza el valor del dispositivo"""
    c.execute('UPDATE dispositivo SET dispositivo = ?, valor = ? WHERE id = ?', (dispositivo.nombre, dispositivo.valor, id))
    conn.commit()
    return {"mensaje": "Dispositivo actualizado correctamente"}