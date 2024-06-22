import tkinter as tk
from tkinter import messagebox
from tipos_gerencimanto_memoria.paginacao import Paginacao

class InterfacePaginacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Gerenciamento de Memória Paginada")
        self.geometry("800x600")

        self.tamanho_total = tk.IntVar()
        self.tamanho_pagina = tk.IntVar()

        self.center_window(800, 600)
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.label_tamanho_total = tk.Label(self, text="Tamanho Total da Memória:")
        self.label_tamanho_total.pack(pady=10)

        self.entry_tamanho_total = tk.Entry(self, textvariable=self.tamanho_total)
        self.entry_tamanho_total.pack(pady=5)

        self.label_tamanho_pagina = tk.Label(self, text="Tamanho de Cada Página:")
        self.label_tamanho_pagina.pack(pady=10)

        self.entry_tamanho_pagina = tk.Entry(self, textvariable=self.tamanho_pagina)
        self.entry_tamanho_pagina.pack(pady=5)

        self.btn_iniciar = tk.Button(self, text="Iniciar", command=self.iniciar_paginacao)
        self.btn_iniciar.pack(pady=10)

    def iniciar_paginacao(self):
        try:
            tamanho_total = self.tamanho_total.get()
            tamanho_pagina = self.tamanho_pagina.get()
            if tamanho_total <= 0 or tamanho_pagina <= 0:
                raise ValueError
            self.paginacao = Paginacao(tamanho_total, tamanho_pagina)
            self.abrir_painel_paginacao()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos para a memória e o tamanho da página.")

    def abrir_painel_paginacao(self):
        self.clear_frame()

        self.label_id = tk.Label(self, text="ID do Processo:")
        self.label_id.pack(pady=5)

        self.entry_id = tk.Entry(self)
        self.entry_id.pack(pady=5)

        self.label_tamanho_processo = tk.Label(self, text="Tamanho do Processo:")
        self.label_tamanho_processo.pack(pady=5)

        self.entry_tamanho_processo = tk.Entry(self)
        self.entry_tamanho_processo.pack(pady=5)

        self.btn_alocar = tk.Button(self, text="Alocar", command=self.alocar_memoria)
        self.btn_alocar.pack(pady=5)

        self.btn_desalocar = tk.Button(self, text="Desalocar", command=self.desalocar_memoria)
        self.btn_desalocar.pack(pady=5)

        self.btn_limpar = tk.Button(self, text="Limpar", command=self.limpar_memoria)
        self.btn_limpar.pack(pady=5)

        self.memory_canvas = tk.Canvas(self, width=800, height=400, bg="white")
        self.memory_canvas.pack(pady=10)

        self.display_memory()

    def alocar_memoria(self):
        try:
            process_id = self.entry_id.get().strip()
            tamanho = int(self.entry_tamanho_processo.get().strip())
            #Limpa os campos de id e tamanho assim que o botão 'Alocar' é pressionado
            self.entry_id.delete(0, tk.END)
            self.entry_tamanho_processo.delete(0, tk.END)

            if self.paginacao.aloca(process_id, tamanho):
                messagebox.showinfo("Sucesso", "Memória alocada com sucesso.")
            else:
                messagebox.showwarning("Falha", "Falha ao alocar memória.")
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Use o formato 'ID, Tamanho'.")
        self.display_memory()

    def desalocar_memoria(self):
        process_id = self.entry_id.get().strip()
        # Limpa o campo de id assim que o botão de 'Desalocar' é pressionado
        self.entry_id.delete(0, tk.END)
        
        if self.paginacao.desaloca(process_id):
            messagebox.showinfo("Sucesso", "Memória desalocada com sucesso.")
        else:
            messagebox.showwarning("Falha", "Falha ao desalocar memória.")
        self.display_memory()

    def limpar_memoria(self):
        self.paginacao = Paginacao(self.paginacao.tamanho_total, self.paginacao.tamanho_pagina)
        messagebox.showinfo("Sucesso", "Memória limpa com sucesso.")
        self.display_memory()

    def display_memory(self):
        self.memory_canvas.delete("all")
        num_paginas = len(self.paginacao.memoria)
        pagina_height = 30

        for i, pagina in enumerate(self.paginacao.memoria):
            y1 = i * pagina_height
            y2 = y1 + pagina_height

            if pagina is None:
                fill_color = "lightblue"
                text = f"P{i + 1}: Livre"
            else:
                fill_color = "pink"
                text = f"P{i + 1}: Processo: {pagina.localizacao_pagina_virtual}"

            self.memory_canvas.create_rectangle(0, y1, 800, y2, fill=fill_color)
            self.memory_canvas.create_text(400, (y1 + y2) / 2, text=text)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = InterfacePaginacao()
    app.mainloop()