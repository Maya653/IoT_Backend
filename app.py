import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

conn = sqlite3.connect("dispositivo.db")
c = conn.cursor()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
    allow_credentials = True
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

@app.get("/dispositivo{valor}")
async def obtener_dispositivo(valor: str):
    """obtiene un valor  """
    c.execute('SELECT * FROM dispositivo WHERE valor = ?', (valor,))
    row = c.fetchone()
    if row:
        dispositivo = {"id": row[0], "nombre": row[1], "valor": row[2]}
        return dispositivo
    else:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")


@app.put("dispositivo/{valor}")
async def actualizar_dispositivo(valor: str, dipositivo: Dispositivo):
    """Actualiza el valor del dispositivo"""
    c.execute('UPDATE dispositivo SET  nombre = ?, valor= ? WHERE valor = ?',
               (dispositivo.nombre, dispositivo.valor, valor))
    conn.commit()
    return {"mensaje": "Dispositivo actualizando correctamente"}