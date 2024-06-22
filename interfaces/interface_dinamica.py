import tkinter as tk
from tkinter import messagebox
from tipos_gerencimanto_memoria.alocacao_particionada.dinamica import Dinamica

class InterfaceDinamica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Gerenciamento de Memória Dinâmica")
        self.geometry("800x600")

        self.tamanho_total = tk.IntVar()
        self.dinamica = None

        self.center_window(800, 600)
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.label = tk.Label(self, text="Qual o tamanho total da memória?")
        self.label.pack(pady=10)

        self.memory_size_entry = tk.Entry(self, textvariable=self.tamanho_total)
        self.memory_size_entry.pack(pady=5)

        self.btn_next = tk.Button(self, text="Próximo", command=self.setup_memory)
        self.btn_next.pack(pady=5)

    def setup_memory(self):
        self.clear_frame()
        self.dinamica = Dinamica(self.tamanho_total.get())
        self.create_memory_interface()

    def create_memory_interface(self):
        self.label = tk.Label(self, text="Gerenciamento de Memória Dinâmica")
        self.label.pack(pady=10)

        self.label_id = tk.Label(self, text="ID do Processo:")
        self.label_id.pack(pady=5)

        self.entry_id = tk.Entry(self)
        self.entry_id.pack(pady=5)

        self.label_tamanho = tk.Label(self, text="Tamanho do Processo:")
        self.label_tamanho.pack(pady=5)

        self.entry_tamanho = tk.Entry(self)
        self.entry_tamanho.pack(pady=5)

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
            tamanho = int(self.entry_tamanho.get().strip())
            #Limpa os campos de id e tamanho assim que o botão 'Alocar' é pressionado
            self.entry_id.delete(0, tk.END)
            self.entry_tamanho.delete(0, tk.END)
            if self.dinamica.alocar(process_id, tamanho):
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
        if self.dinamica.desalocar(process_id):
            messagebox.showinfo("Sucesso", "Memória desalocada com sucesso.")
        else:
            messagebox.showwarning("Falha", "Falha ao desalocar memória.")
        self.display_memory()

    def limpar_memoria(self):
        self.dinamica = Dinamica(self.tamanho_total.get())
        messagebox.showinfo("Sucesso", "Memória limpa com sucesso.")
        self.display_memory()

    def display_memory(self):
        self.memory_canvas.delete("all")
        total_height = 400
        total_width = 800
        used_height = 0

        for block in self.dinamica.memoria:
            if len(block) == 2:
                start, size = block
                color = "lightblue"
                text = f"Livre: {size}"
            else:
                start, size, process_id = block
                color = "pink"
                text = f"ID: {process_id}, Tamanho: {size}"

            height_ratio = size / self.dinamica.tamanho_memoria
            block_height = height_ratio * total_height

            self.memory_canvas.create_rectangle(0, used_height, total_width, used_height + block_height, fill=color)
            self.memory_canvas.create_text(total_width / 2, used_height + block_height / 2, text=text)

            used_height += block_height

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = InterfaceDinamica()
    app.mainloop()
