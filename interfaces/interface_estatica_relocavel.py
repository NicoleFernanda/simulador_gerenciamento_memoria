import tkinter as tk
from tkinter import messagebox
from tipos_gerencimanto_memoria.alocacao_particionada.estatica_relocavel import EstaticaRelocavel

class InterfaceEstatica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Gerenciamento de Memória Estática Relocável")
        self.geometry("800x600")

        self.partition_count = tk.IntVar()
        self.current_partition = 1
        self.partitions = []

        self.center_window(800, 600)
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.label = tk.Label(self, text="Quantas partições?")
        self.label.pack(pady=10)

        self.partition_entry = tk.Entry(self, textvariable=self.partition_count)
        self.partition_entry.pack(pady=5)

        self.btn_next = tk.Button(self, text="Próximo", command=self.setup_partitions)
        self.btn_next.pack(pady=5)

    def setup_partitions(self):
        self.clear_frame()
        self.partitions = []
        self.current_partition = 1
        self.prompt_partition_size()

    def prompt_partition_size(self):
        self.clear_frame()
        if self.current_partition <= self.partition_count.get():
            self.label = tk.Label(self, text=f"Tamanho da partição {self.current_partition}:")
            self.label.pack(pady=10)

            self.size_entry = tk.Entry(self)
            self.size_entry.pack(pady=5)

            self.btn_next = tk.Button(self, text="Próximo", command=self.add_partition)
            self.btn_next.pack(pady=5)
        else:
            self.create_estatica()

    def add_partition(self):
        try:
            size = int(self.size_entry.get())
            self.partitions.append(size)
            self.current_partition += 1
            self.prompt_partition_size()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido.")

    def create_estatica(self):
        self.clear_frame()
        self.estatica = EstaticaRelocavel(self.partitions)

        self.label = tk.Label(self, text="Gerenciamento de Partições Estáticas")
        self.label.pack(pady=10)

        self.label_id = tk.Label(self, text="ID do Processo:")
        self.label_id.pack(pady=5)

        self.entry_id = tk.Entry(self)
        self.entry_id.pack(pady=5)

        self.label_tamanho = tk.Label(self, text="Tamanho do Processo:")
        self.label_tamanho.pack(pady=5)

        self.entry_tamanho = tk.Entry(self)
        self.entry_tamanho.pack(pady=5)

        self.btn_alocar = tk.Button(self, text="Alocar", command=self.alocar_estatica)
        self.btn_alocar.pack(pady=5)

        self.btn_desalocar = tk.Button(self, text="Desalocar", command=self.desalocar_estatica)
        self.btn_desalocar.pack(pady=5)

        self.btn_limpar = tk.Button(self, text="Limpar", command=self.limpar_memoria)
        self.btn_limpar.pack(pady=5)

        self.memory_canvas = tk.Canvas(self, width=800, height=400, bg="white")
        self.memory_canvas.pack(pady=10)

        self.display_memory()

    def alocar_estatica(self):
        try:
            process_id = self.entry_id.get().strip()
            tamanho = int(self.entry_tamanho.get().strip())

            #Limpa os campos de id e tamanho assim que o botão 'Alocar' é pressionado
            self.entry_id.delete(0, tk.END)
            self.entry_tamanho.delete(0, tk.END)

            if self.estatica.alocar(process_id, tamanho):
                messagebox.showinfo("Sucesso", "Memória alocada com sucesso.")
            else:
                messagebox.showwarning("Falha", "Falha ao alocar memória.")
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Use o formato 'ID, Tamanho'.")
        self.display_memory()

    def desalocar_estatica(self):
        process_id = self.entry_id.get().strip()

        #Limpa o campo de id assim que o botão 'Alocar' é pressionado
        self.entry_id.delete(0, tk.END)
        
        if self.estatica.desalocar(process_id):
            messagebox.showinfo("Sucesso", "Memória desalocada com sucesso.")
        else:
            messagebox.showwarning("Falha", "Falha ao desalocar memória.")
        self.display_memory()

    def limpar_memoria(self):
        self.estatica = EstaticaRelocavel(self.partitions)
        messagebox.showinfo("Sucesso", "Memória limpa com sucesso.")
        self.display_memory()

    def display_memory(self):
        self.memory_canvas.delete("all")
        num_partitions = len(self.estatica.particoes)
        partition_height = 30  # Altura reduzida para cada partição

        for i, block in enumerate(self.estatica.memoria):
            y1 = i * partition_height
            y2 = y1 + partition_height
            width_ratio = 1

            # Calcular largura do retângulo proporcional ao tamanho da partição
            if block is None:
                fill_color = "lightblue"
                partition_size = self.estatica.particoes[i]
            else:
                fill_color = "pink"
                partition_size = block[1]
                width_ratio = partition_size / self.estatica.particoes[i]


              # proporção do tamanho da partição
            x1 = 0
            x2 = 800 * width_ratio

            # Desenhar retângulo da partição
            self.memory_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)

            # Texto dentro do retângulo
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            if block is None:
                text = f"P{i + 1}: Livre, Tamanho: {partition_size}"
            else:
                text = f"P[{i + 1}] : Processo: [{block[0]}], Tamanho: [{block[1]}]"
            self.memory_canvas.create_text(text_x, text_y, text=text)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = InterfaceEstatica()
    app.mainloop()