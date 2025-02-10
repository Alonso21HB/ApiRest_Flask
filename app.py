from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


class Tarea:
    def __init__(self, id: int, titulo: str, descripcion: str):
        self.id = id
        self.titulo  = titulo
        self.descripcion = descripcion
    
    def diccionario(self):
        return{
            "id":self.id,
            "titulo": self.titulo,
            "descripcion":self.descripcion
        }
    
tareas = [
    Tarea(1, "Aprender Flask", "Estudiar los fundamentos de Flask"),
    Tarea(2, "Leer un libro","Leer un libro de desarrollo web")
]

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    return jsonify([tarea.diccionario() for tarea in tareas])

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    nueva_tarea = Tarea(id=request.json['id'],
                        titulo = request.json['titulo'],
                        descripcion=request.json['descripcion'])
    tareas.append(nueva_tarea)
    return jsonify(nueva_tarea.diccionario()), 201

@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tarea = next((t for t in tareas if t.id == id), None)
    if tarea is not None:
        tarea.titulo = request.json.get('titulo', tarea.titulo)
        tarea.descripcion = request.json.get('descripcion', tarea.descripcion)
        return jsonify(tarea.diccionario())
    return jsonify({"error": "no hay nada de cambios"}), 404

@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    global tareas
    tareas = [t for t in tareas if t.id != id]
    return jsonify({'resultado': True})
if __name__ == '__main__':
    app.run(debug=True)