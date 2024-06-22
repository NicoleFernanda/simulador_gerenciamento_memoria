class Dinamica:
    def __init__(self, tamanho_total):
        self.tamanho_memoria = tamanho_total
        self.memoria = [(0, tamanho_total)]  # inicializa a lista memory com um único bloco livre que cobre toda a memória disponível
        # cada bloco (assim como em alocacao estatica) é representado por uma tupla (start_address, size)

    # se o bloco livre for maior do que o necessário, ele cria um novo bloco livre com o espaço restante (linha 14 e 15)
    def alocar(self, id, tamanho):
        for i, bloco in enumerate(self.memoria):
            if len(bloco) == 2:  # Verifica se o bloco é livre (se for livre, tera apenas 2 params dentro do tupla, se nao, tera 3)
                endereco_incial, tamanho_bloco = bloco
                if tamanho_bloco >= tamanho:
                    self.memoria[i] = (endereco_incial, tamanho, id)
                    if tamanho_bloco > tamanho:
                        self.memoria.insert(i + 1, (endereco_incial + tamanho, tamanho_bloco - tamanho)) # cria um novo bloco com o que sobrou
                    return True
        return False

    def desalocar(self, process_id):
        for i, bloco in enumerate(self.memoria):
            if len(bloco) == 3 and bloco[2] == process_id:
                endereco_incial, tamanho_bloco, _ = bloco # desempacota o bloco
                self.memoria[i] = (endereco_incial, tamanho_bloco) # marca o bloco como livre
                # juntar blocos lu=ivres adjacentes
                if i > 0 and len(self.memoria[i - 1]) == 2: # verifica se existe bloco anterior e se le esta livre (checar linha 10, segue basicamente o mesmo principio)
                    end_incial_a, tamanho_a = self.memoria.pop(i - 1) # remove o bloco livre anterior e obtém seu endereço inicial e tamanho
                    self.memoria[i - 1] = (end_incial_a, tamanho_a + tamanho_bloco)
                    # atualiza o bloco anterior na lista de memória, aumentando seu tamanho para incluir o tamanho do bloco que foi desalocado

                if i < len(self.memoria) - 1 and len(self.memoria[i + 1]) == 2: # agora verifica se tem algum após ele livre
                    end_inicial_p, tamanho_p = self.memoria.pop(i + 1) # remove o bloco livre posterior e obtém seu endereço inicial e tamanho
                    self.memoria[i] = (endereco_incial, tamanho_bloco + tamanho_p)
                    # atualiza o bloco atual na lista de memória, aumentando seu tamanho para incluir o tamanho do bloco posterior que foi removido
                return True
        return False


# _a = anterior
# _p = posterior