from collections import deque

class Pagina:
    def __init__(self, localizacao_pagina_virtual, numero_quadro_fisico=None, valid=0):
        self.localizacao_pagina_virtual = localizacao_pagina_virtual  # armazena o numero da pagina virtual
        self.numero_quadro_fisico = numero_quadro_fisico  # armazena o numero do quadro fisico associdado
        self.validade = valid  # indica se a pagina é valida (0 ou 1)
        # esses dois parametros são, basicamente, para fazer o mapeamento. como mantemos o código
        # simples, teoricamente, não precisaríamos dessas informações. a não ser para aprimorar futuramente


class Paginacao:
    def __init__(self, tamanho_total, tamanho_pagina):
        self.tamanho_total = tamanho_total  # define o tamanho total da memoria
        self.tamanho_pagina = tamanho_pagina  # define o tamanho total de cada pagina
        self.numero_paginas = tamanho_total // tamanho_pagina  # calcula o número total de páginas dividindo o tamanho total da memória pelo tamanho da página
        self.memoria = [None] * self.numero_paginas  # lista com um comprimento igual ao número de páginas (inciada com nada) -> memoria
        self.ids = deque()

    def aloca(self, id, tamanho):

        # verifica, pelo tamanho do meu processo a ser alocado, o tamanho de paginas necessárias
        # paginas_necessarias = (tamanho // self.tamanho_pagina) + (1 if tamanho % self.tamanho_pagina else 0) # 1 + resto
        existe_pagina_vazia = False
        paginas_alocadas = []  # cria uma lista vazia para armazenar os indices das paginas alocadas
        for i in range(self.numero_paginas):  # percorre todas as paginas
            if self.memoria[i] is None:  # verifica se a pagina atual esta livre
                existe_pagina_vazia = True
                self.memoria[i] = Pagina(id)  # cria-se uma pagina
                paginas_alocadas.append(i)  # adiciona o indice naquela lista allocated_pages vazia criada na linha 9
                tamanho = tamanho - self.tamanho_pagina

                if tamanho <= 0:
                    # eu adiciono numa pilha o id - fifo
                    self.ids.append(id)
                    return paginas_alocadas
                    # verifica se o número de páginas alocadas é igual ao número de páginas necessárias (num_pages).
                    # Se sim, retorna a lista allocated_pages com os índices das páginas alocadas.

        # Rollback if not enough pages were found
        # Se não houver páginas suficientes para alocar, inicia um rollback: (caso de processo parcial)
        # para cada página na lista allocated_pages, define a página como None, liberando-a.

        if existe_pagina_vazia:
            for pagina in paginas_alocadas:
                self.memoria[pagina] = None
            return None
        else:
            self.desaloca(self.ids.popleft()) # significa que não existe pagina livre e preciso desalocar para alocar
            return self.aloca(id, tamanho)

    def desaloca(self, id):
        desalocou = False
        for i in range(self.numero_paginas):
            if isinstance(self.memoria[i], Pagina) and self.memoria[i].localizacao_pagina_virtual == id:
                self.memoria[i] = None
                desalocou = True

        return desalocou


# Quando um processo solicita memória, ele especifica quanto precisa.
# No esquema de paginação, essa quantidade é traduzida para um número de páginas.
# O objetivo do método alocar é encontrar e reservar esse número de páginas contíguas (ou não)
# para o processo.
# Um processo pode necessitar de várias páginas para funcionar corretamente.
# Se, por exemplo, um processo precisa de 3 páginas, mas apenas 2 estão disponíveis,
# o processo não poderá ser executado corretamente.
# A verificação garante que o processo receba exatamente o que solicitou.
