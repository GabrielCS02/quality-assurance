from locust import HttpUser, task, between

class ClienteEFecaf(HttpUser):
    # Simula o tempo que um cliente real demora a ler a página (entre 1 a 3 segundos)
    wait_time = between(1.0, 3.0)

    @task(3) # Peso 3: É 3 vezes mais provável o cliente visitar a página inicial
    def visitar_home(self):
        self.client.get("/")

    @task(1) # Peso 1: Menos provável, mas os clientes vão ao checkout
    def fazer_checkout(self):
        # Aqui é onde configurámos aquele gargalo de performance de 15% de chance de erro!
        self.client.get("/checkout")