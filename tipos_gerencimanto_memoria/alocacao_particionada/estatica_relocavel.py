class EstaticaRelocavel:

    def __init__(self, particoes):  # entra com uma lista com os tamanhos das particoes
        self.particoes = particoes
        self.memoria = (
                    [None] * len(particoes))  # inicializa a memoria para que tenha o mesmo tamanho da particoes fixas

    def alocar(self, id, tamanho):
        for i, tamanho_particao in enumerate(self.particoes):  # indice e valor = enumerate
            if self.memoria[i] is None and tamanho_particao >= tamanho:  # se não tiver nada alocado na memoria e o tamanho for ideal
                self.memoria[i] = (id, tamanho)  # insere na memoria
                return True  # retorna true
        return False

    def desalocar(self, id):
        for i, bloco in enumerate(self.memoria):  # percorre a minha memoria (as com valores alocados)
            if bloco is not None and bloco[0] == id:  # bloco[0] se refere ao id daquela particao alocada
                self.memoria[i] = None
                return True
        return False
