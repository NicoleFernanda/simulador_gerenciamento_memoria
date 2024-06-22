class Segmento:
    def __init__(self, id, endereco_inicial, tamanho): # incializa um segmento, com seu id, endereco incial e tamanho
        self.id = id
        self.endereco_inicial = endereco_inicial
        self.tamanho = tamanho

class Segmentacao:
    def __init__(self, tamanho_total):
        self.tamanho_total = tamanho_total # tamanho total da memoria
        self.memoria = [Segmento(None, 1, tamanho_total)]  # inicialmente, um segmento grande livre
        # uma lista que contém os segmentos de mamória

    def alocar(self, id, alocar_tamanho):
        for segmento in self.memoria: # percorre cada segmento na lista de memoria
            if segmento.id is None and segmento.tamanho >= alocar_tamanho: # verifica se é livre e se tem tamanho suficiente
                new_segment = Segmento(id, segmento.endereco_inicial, (alocar_tamanho - 1))
                # atualiza o endereco inicial daquele segmento
                segmento.endereco_inicial = segmento.endereco_inicial + alocar_tamanho # determina o endereco de inicio daquele processo, caso já exista outros processo inseridos
                # endereco absoluto
                segmento.tamanho = segmento.tamanho - (alocar_tamanho - 1) # atualiza o segmento existente para refletir a reducao de espaco livre
                if segmento.tamanho == 0:
                    self.memoria.remove(segmento) # nao tem pq eu deixar um segmento de tamanho 0
                self.memoria.append(new_segment) # adiciona novo segmento criado
                return True
        return False

    def desalocar(self, id):
        for segmento in self.memoria:
            if segmento.id == id:
                segmento.id = None # marca segmento como livre
                self.junta_segmentos_livres() # reune segmentos livres adjacentes
                return True
        return False

    def junta_segmentos_livres(self):
        self.memoria.sort(key=lambda s: s.endereco_inicial) # ordena os segmentos pela posicao incial
        i = 0
        while i < len(self.memoria) - 1:
            if self.memoria[i].id is None and self.memoria[i + 1].id is None: # se dois segmentos adj estao livres
                self.memoria[i].tamanho += self.memoria[i + 1].tamanho
                self.memoria.pop(i + 1) # remove esse segmento, pois "os dois estao em um segmento apenas"
            else:
                i += 1
