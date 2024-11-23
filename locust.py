from locust import HttpUser, task, events
import subprocess
import signal

class CustomUser(HttpUser):
    wait_time = lambda self: 1  # Intervalo entre tareas (puedes ajustarlo si quieres)

    @task
    def start_xnxx(self):
        # No se ejecuta ninguna tarea directa aquí
        pass

# Variable global para manejar el proceso del script
xnxx_process = None

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    Este evento se ejecuta cuando iniciamos la prueba desde la interfaz de Locust.
    """
    global xnxx_process
    url = environment.host  # Obtener la URL ingresada en la interfaz de Locust

    if url:
        print(f"Iniciando xnxx.js con la URL: {url}")
        xnxx_process = subprocess.Popen(
            ["node", "ps2.js", url, "proxy"],  # Ejecuta el script con la URL y modo "proxy"
            stdout=subprocess.PIPE,  # Captura la salida estándar (opcional)
            stderr=subprocess.PIPE   # Captura los errores (opcional)
        )
    else:
        print("No se definió una URL en la interfaz de Locust.")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Este evento se ejecuta cuando detenemos la prueba desde la interfaz de Locust.
    """
    global xnxx_process
    if xnxx_process:
        print("Deteniendo xnxx.js...")
        xnxx_process.send_signal(signal.SIGTERM)  # Enviar señal para terminar el proceso
        try:
            xnxx_process.wait(timeout=5)  # Esperar hasta 5 segundos a que el proceso termine
        except subprocess.TimeoutExpired:
            print("El proceso no respondió, forzando terminación")
            xnxx_process.kill()  # Forzar el cierre del proceso si no responde
        xnxx_process = None
