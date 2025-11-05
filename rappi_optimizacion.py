import random
import time
from datetime import datetime, timedelta

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
    
    def medir_tiempo_ejecucion(self, funcion, *args):
        """Mide el tiempo de ejecución de una función"""
        inicio = time.time()
        resultado = funcion(*args)
        fin = time.time()
        return resultado, fin - inicio

# Función principal para demostración
def demostrar_algoritmos():
    gestor = GestorPedidos()
    
    print("=== OPTIMIZACIÓN ALGORÍTMICA RAPPI ===\n")
    
    # Generar datos de prueba
    print("Generando 100 pedidos de prueba...")
    gestor.generar_pedidos_aleatorios(100)
    print(f"Se generaron {len(gestor.pedidos)} pedidos\n")
    
    # PRUEBAS DE BÚSQUEDA
    print("--- PRUEBAS DE BÚSQUEDA ---")
    
    # Búsqueda lineal
    repartidor_buscar = 150
    resultados_lineal, pasos_lineal = gestor.busqueda_lineal_repartidor(repartidor_buscar)
    print(f"Búsqueda Lineal - Repartidor {repartidor_buscar}:")
    print(f"  Pedidos encontrados: {len(resultados_lineal)}")
    print(f"  Pasos ejecutados: {pasos_lineal}")
    print(f"  Complejidad: O(n)\n")
    
    # Búsqueda binaria
    pedido_buscar = 50
    resultado_binaria, pasos_binaria = gestor.busqueda_binaria_pedido(pedido_buscar)
    print(f"Búsqueda Binaria - Pedido {pedido_buscar}:")
    if resultado_binaria:
        print(f"  Pedido encontrado: {resultado_binaria}")
    else:
        print(f"  Pedido no encontrado")
    print(f"  Pasos ejecutados: {pasos_binaria}")
    print(f"  Complejidad: O(log n)\n")
    
    # PRUEBAS DE ORDENAMIENTO
    print("--- PRUEBAS DE ORDENAMIENTO ---")
    
    # Ordenamiento burbuja
    pedidos_ordenados_burbuja, pasos_burbuja = gestor.ordenamiento_burbuja()
    print(f"Ordenamiento Burbuja:")
    print(f"  Pasos ejecutados: {pasos_burbuja}")
    print(f"  Complejidad: O(n²)")
    print(f"  Primeros 5 pedidos ordenados:")
    for i in range(min(5, len(pedidos_ordenados_burbuja))):
        print(f"    {pedidos_ordenados_burbuja[i]}")
    print()
    
    # Ordenamiento por inserción
    pedidos_ordenados_insercion, pasos_insercion = gestor.ordenamiento_insercion()
    print(f"Ordenamiento por Inserción:")
    print(f"  Pasos ejecutados: {pasos_insercion}")
    print(f"  Complejidad: O(n²) - pero más eficiente")
    print(f"  Primeros 5 pedidos ordenados:")
    for i in range(min(5, len(pedidos_ordenados_insercion))):
        print(f"    {pedidos_ordenados_insercion[i]}")
    print()
    
    # COMPARACIÓN DE EFICIENCIA
    print("--- COMPARACIÓN DE EFICIENCIA ---")
    print(f"Búsqueda Lineal vs Binaria:")
    print(f"  Diferencia en pasos: {pasos_lineal - pasos_binaria} pasos")
    print(f"  Búsqueda binaria fue {pasos_lineal/pasos_binaria if pasos_binaria > 0 else 'infinitamente'} más eficiente")
    print()
    print(f"Ordenamiento Burbuja vs Inserción:")
    print(f"  Diferencia en pasos: {pasos_burbuja - pasos_insercion} pasos")
    print(f"  Inserción fue {pasos_burbuja/pasos_insercion if pasos_insercion > 0 else 'infinitamente'} más eficiente")

# Función para pruebas con diferentes tamaños de datos
def prueba_escalabilidad():
    """Prueba cómo escalan los algoritmos con diferentes tamaños de datos"""
    print("\n=== PRUEBA DE ESCALABILIDAD ===")
    
    tamanios = [10, 50, 100, 500, 1000]
    
    for tamanio in tamanios:
        gestor = GestorPedidos()
        gestor.generar_pedidos_aleatorios(tamanio)
        
        # Medir búsqueda lineal
        _, pasos_lineal = gestor.busqueda_lineal_repartidor(999)
        
        # Medir búsqueda binaria
        _, pasos_binaria = gestor.busqueda_binaria_pedido(tamanio // 2)
        
        # Medir ordenamientos
        _, pasos_burbuja = gestor.ordenamiento_burbuja()
        _, pasos_insercion = gestor.ordenamiento_insercion()
        
        print(f"\nTamaño: {tamanio} pedidos")
        print(f"  Búsqueda Lineal: {pasos_lineal} pasos")
        print(f"  Búsqueda Binaria: {pasos_binaria} pasos")
        print(f"  Ordenamiento Burbuja: {pasos_burbuja} pasos")
        print(f"  Ordenamiento Inserción: {pasos_insercion} pasos")

if __name__ == "__main__":
    demostrar_algoritmos()
    prueba_escalabilidad()