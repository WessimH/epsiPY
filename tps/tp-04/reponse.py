import asyncio
import hashlib
import multiprocessing
import random
import threading
import time


def exo1(k: int) -> list[str]:
    threads = []
    res = []

    def run():
        res.append(threading.current_thread().name)

    for i in range(k):
        threads.append(threading.Thread(target=run))
        threads[-1].start()

    for thread in threads:
        thread.join()
    return res


# Fonction pour vérifier si un nombre est premier
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n / 2 + 1)):
        if n % i == 0:
            return False
    return True


def exo2(numbers: list[int]) -> list[bool]:
    # Utiliser Pool pour paralléliser la vérification
    with multiprocessing.Pool() as pool:
        results = pool.map(is_prime, numbers)

    return results


class WaitAndValidateTask:
    def __init__(self):
        self.start_time = None

    def ask(self):
        self.start_time = time.time()
        self.wait_time = random.randint(3, 5)
        return self.wait_time

    def validate(self):
        if self.start_time is None:
            raise RuntimeError("ask() must be called before validate()")


async def exo3(task_instances):
    # Créer une liste pour stocker les temps d'attente
    wait_times = []

    async def ask_and_wait(instance):
        wait_time = instance.ask()
        wait_times.append(wait_time)
        await asyncio.sleep(wait_time)  # Attendre le temps spécifié

    # Appeler ask() de manière concurrente pour toutes les instances
    tasks = [ask_and_wait(instance) for instance in task_instances]
    await asyncio.gather(*tasks)

    # Valider après que toutes les `ask` ont été traitées
    for instance in task_instances:
        instance.validate()


class ProcessPool:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.tasks = multiprocessing.Queue()
        self.results = multiprocessing.Queue()
        self.processes = []

    def worker(self):
        while True:
            item = self.tasks.get()
            if item is None:  # Condition pour sortir
                break
            # Calculer le MD5
            md5_hash = hashlib.md5(str(item).encode()).hexdigest()
            self.results.put(md5_hash)

    def __enter__(self):
        processes = []
        for _ in range(self.num_processes):
            p = multiprocessing.Process(target=self.worker)
            p.start()
            processes.append(p)
        self.processes = processes
        return self.tasks

    def __exit__(self, exc_type, exc_val, exc_tb):
        for _ in self.processes:
            self.tasks.put(None)  # Indiquer aux workers de sortir
        for p in self.processes:
            p.join()

    def add_task(self, item):
        self.tasks.put(item)

    def get_results(self):
        results = []
        while not self.results.empty():
            results.append(self.results.get())
        return results
