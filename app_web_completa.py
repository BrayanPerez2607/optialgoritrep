from flask import Flask, render_template, request, jsonify
import random
import time
import matplotlib
matplotlib.use('Agg')  # Para que matplotlib funcione en Flask
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

# Clase para representar un pedido
class Pedido:
    def __init__(self, id, prioridad, repartidor_id=None, direccion=""):
        self.id = id
        self.prioridad = prioridad  # 1: Alta, 2: Media, 3: Baja
        self.repartidor_id = repartidor_id
        self.direccion = direccion
        self.fecha_creacion = datetime.now()
    
    def __str__(self):
        return f"Pedido {self.id} - Prioridad: {self.prioridad} - Repartidor: {self.repartidor_id}"

# Clase para gestionar pedidos
class GestorPedidos:
    def __init__(self):
        self.pedidos = []
        self.contador_pasos = 0
    
    def agregar_pedido(self, pedido):
        self.pedidos.append(pedido)
    
    def generar_pedidos_aleatorios(self, cantidad):
        """Genera pedidos de prueba"""
        self.pedidos = []  # Reiniciar la lista
        for i in range(cantidad):
            prioridad = random.randint(1, 3)
            repartidor = random.randint(100, 999) if random.random() > 0.3 else None
            pedido = Pedido(i + 1, prioridad, repartidor, f"Calle {random.randint(1, 100)}")
            self.agregar_pedido(pedido)
    
    # ALGORITMOS DE BÚSQUEDA
    
    def busqueda_lineal_repartidor(self, repartidor_id):
        """Búsqueda lineal O(n) - Encuentra todos los pedidos de un repartidor"""
        self.contador_pasos = 0
        resultados = []
        
        for pedido in self.pedidos:
            self.contador_pasos += 1
            if pedido.repartidor_id == repartidor_id:
                resultados.append(pedido)
        
        return resultados, self.contador_pasos
    
    def busqueda_binaria_pedido(self, pedido_id):
        """Búsqueda binaria O(log n) - Requiere lista ordenada"""
        self.contador_pasos = 0
        
        # Primero ordenamos por ID (para búsqueda binaria)
        pedidos_ordenados = sorted(self.pedidos, key=lambda x: x.id)
        
        izquierda, derecha = 0, len(pedidos_ordenados) - 1
        
        while izquierda <= derecha:
            self.contador_pasos += 1
            medio = (izquierda + derecha) // 2
            
            if pedidos_ordenados[medio].id == pedido_id:
                return pedidos_ordenados[medio], self.contador_pasos
            elif pedidos_ordenados[medio].id < pedido_id:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        
        return None, self.contador_pasos
    
    # ALGORITMOS DE ORDENAMIENTO
    
    def ordenamiento_burbuja(self):
        """Ordenamiento burbuja O(n²) - Ordena por prioridad"""
        self.contador_pasos = 0
        pedidos_copia = self.pedidos.copy()
        n = len(pedidos_copia)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                self.contador_pasos += 1
                if pedidos_copia[j].prioridad > pedidos_copia[j + 1].prioridad:
                    pedidos_copia[j], pedidos_copia[j + 1] = pedidos_copia[j + 1], pedidos_copia[j]
        
        return pedidos_copia, self.contador_pasos
    
    def ordenamiento_insercion(self):
        """Ordenamiento por inserción O(n²) pero más eficiente que burbuja"""
        self.contador_pasos = 0
        pedidos_copia = self.pedidos.copy()
        
        for i in range(1, len(pedidos_copia)):
            clave = pedidos_copia[i]
            j = i - 1
            
            while j >= 0 and pedidos_copia[j].prioridad > clave.prioridad:
                self.contador_pasos += 1
                pedidos_copia[j + 1] = pedidos_copia[j]
                j -= 1
            
            pedidos_copia[j + 1] = clave
            self.contador_pasos += 1
        
        return pedidos_copia, self.contador_pasos

# Instancia global del gestor de pedidos
gestor = GestorPedidos()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_pedidos', methods=['POST'])
def generar_pedidos():
    cantidad = int(request.form['cantidad'])
    gestor.generar_pedidos_aleatorios(cantidad)
    return jsonify({
        'mensaje': f'Se generaron {cantidad} pedidos exitosamente.',
        'total_pedidos': len(gestor.pedidos)
    })

@app.route('/busqueda_lineal', methods=['POST'])
def busqueda_lineal():
    repartidor_id = int(request.form['repartidor_id'])
    resultados, pasos = gestor.busqueda_lineal_repartidor(repartidor_id)
    
    resultados_str = [str(pedido) for pedido in resultados]
    
    return jsonify({
        'resultados': resultados_str,
        'pasos': pasos,
        'total_resultados': len(resultados)
    })

@app.route('/busqueda_binaria', methods=['POST'])
def busqueda_binaria():
    pedido_id = int(request.form['pedido_id'])
    resultado, pasos = gestor.busqueda_binaria_pedido(pedido_id)
    
    resultado_str = str(resultado) if resultado else "No encontrado"
    
    return jsonify({
        'resultado': resultado_str,
        'pasos': pasos
    })

@app.route('/ordenamiento_burbuja', methods=['POST'])
def ordenamiento_burbuja():
    pedidos_ordenados, pasos = gestor.ordenamiento_burbuja()
    
    # Tomar solo los primeros 10 para mostrar
    primeros_10 = [str(pedido) for pedido in pedidos_ordenados[:10]]
    
    return jsonify({
        'pedidos_ordenados': primeros_10,
        'pasos': pasos,
        'total_pedidos': len(pedidos_ordenados)
    })

@app.route('/ordenamiento_insercion', methods=['POST'])
def ordenamiento_insercion():
    pedidos_ordenados, pasos = gestor.ordenamiento_insercion()
    
    # Tomar solo los primeros 10 para mostrar
    primeros_10 = [str(pedido) for pedido in pedidos_ordenados[:10]]
    
    return jsonify({
        'pedidos_ordenados': primeros_10,
        'pasos': pasos,
        'total_pedidos': len(pedidos_ordenados)
    })

@app.route('/comparar_algoritmos')
def comparar_algoritmos():
    # Generar gráfico de comparación
    tamanios = [10, 50, 100, 200, 500]
    tiempos_burbuja = []
    tiempos_insercion = []
    pasos_burbuja = []
    pasos_insercion = []
    
    for tamanio in tamanios:
        gestor_temp = GestorPedidos()
        gestor_temp.generar_pedidos_aleatorios(tamanio)
        
        # Medir tiempo de burbuja
        inicio = time.time()
        _, pasos_b = gestor_temp.ordenamiento_burbuja()
        fin = time.time()
        tiempos_burbuja.append(fin - inicio)
        pasos_burbuja.append(pasos_b)
        
        # Medir tiempo de inserción
        inicio = time.time()
        _, pasos_i = gestor_temp.ordenamiento_insercion()
        fin = time.time()
        tiempos_insercion.append(fin - inicio)
        pasos_insercion.append(pasos_i)
    
    # Crear gráfico de tiempos
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(tamanios, tiempos_burbuja, 'o-', label='Burbuja')
    plt.plot(tamanios, tiempos_insercion, 's-', label='Inserción')
    plt.xlabel('Número de pedidos')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Comparación de Tiempos')
    plt.legend()
    plt.grid(True)
    
    # Crear gráfico de pasos
    plt.subplot(1, 2, 2)
    plt.plot(tamanios, pasos_burbuja, 'o-', label='Burbuja')
    plt.plot(tamanios, pasos_insercion, 's-', label='Inserción')
    plt.xlabel('Número de pedidos')
    plt.ylabel('Número de pasos')
    plt.title('Comparación de Pasos')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Convertir gráfico a imagen base64 para mostrar en HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('comparacion.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)