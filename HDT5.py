import statistics
import simpy
import random

res = []

random.seed(25)

class Computer:
    def __init__(self, env, RAM_SIZE, CPU_CAPACITY, CPU_SPEED):
        self.env = env
        self.RAM = simpy.Container(env, init=RAM_SIZE, capacity=RAM_SIZE)
        self.CPU = simpy.Resource(env, capacity=CPU_CAPACITY)
        self.CPU_SPEED = CPU_SPEED

    def execute(self, process):
        instructions_to_execute = min(process.instructions, self.CPU_SPEED)
        yield self.env.timeout(self.CPU_SPEED / instructions_to_execute)
        process.instructions -= instructions_to_execute
        random_io = random.randint(1, 2)
        if random_io == 1:
            print(f"Proceso {process.id} interrumpido por proceso I/O en {self.env.now}")
            yield self.env.timeout(1)
            # Una vez que la I/O ha terminado, el proceso vuelve a estar en estado "Ready"
            print(f"Proceso {process.id} deja el CPU en {env.now}. Hay {process.instructions} instrucciones pendientes.")
            self.env.process(process.ready())
        else:
            print(f"Proceso {process.id} deja el CPU en {env.now}. Hay {process.instructions} instrucciones pendientes.")

class Process:
    def __init__(self, env, id, computer):
        self.id = id
        self.env = env
        self.instructions = random.randint(1, 10)
        self.ram_required = random.randint(1, 10)
        self.computer = computer
        self.start = env.now
        env.process(self.new())
        print(f"Nuevo proceso {self.id} llega al sistema en {self.env.now}.")

    def new(self):
        yield self.computer.RAM.get(self.ram_required)
        print(f"Proceso {self.id} obtiene {self.ram_required} de memoria en {self.env.now}. Hay {self.computer.RAM.level} disponibles")
        self.env.process(self.ready())

    def ready(self):
        print(f"Proceso {self.id} en espera del CPU {self.env.now}")
        with self.computer.CPU.request() as req:
            yield req
            if self.instructions > 0:
                print(f"Proceso {self.id} utilizando el CPU en {self.env.now}")
                yield from self.computer.execute(self)
            else:
                self.terminate()

    def terminate(self):
        print(f"Proceso {self.id} terminado en {self.env.now}")
        self.computer.RAM.put(self.ram_required)
        res.append(env.now - self.start)

def main(env, num_processes):
    computer = Computer(env, 100, 1, 3)
    for i in range(num_processes):
        yield env.timeout(random.expovariate(1.0))
        # Se crea un nuevo proceso
        Process(env, i, computer)

env = simpy.Environment()
env.process(main(env, 200))  # Ejecutar 200 eventos
env.run()

r = 0
for i in res:
    r += i
prom = r / 200
desv = statistics.stdev(res)
print ("El tiempo promedio por proceso es:", prom)
print ("La desviación estándar es:", desv)