import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Cocinero(threading.Thread):
    def __init__(self,numero):
        super().__init__()
        self.name = f'Cocinero {numero}'

    def run(self):
        global platosDisponibles

        while (True):
            semaforoCocinero.acquire()
            try:
                logging.info('Reponiendo los platos...')
                platosDisponibles = 3
            finally:
                semaforoPlato.release()

class Comensal(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.name = f'Comensal {numero}'

    def run(self):
        comensal.acquire()
        try:
            global platosDisponibles
            semaforoPlato.acquire()
            # if platosDisponibles == 0:
            try:
                while platosDisponibles == 0:
                    semaforoCocinero.release()
                    semaforoPlato.acquire()
                platosDisponibles -= 1
                logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
            finally:
                semaforoPlato.release()
        finally:
            comensal.release()


semaforoPlato = threading.Semaphore(1)
semaforoCocinero = threading.Semaphore(0)
comensal = threading.Semaphore(2)

platosDisponibles = 3

cocinero = Cocinero(1)
cocinero.start()



#for i in range(10):
#   Cocinero(i).start()

for i in range(34):
    Comensal(i).start()