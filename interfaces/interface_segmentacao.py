import tkinter as tk
from tkinter import messagebox
from tipos_gerencimanto_memoria.segmentacao import Segmentacao

class InterfaceSegmentacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Gerenciamento de Memória Segmentada")
        self.geometry("800x600")

        self.total_size = tk.IntVar()

        self.center_window(800, 600)
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.label_total_size = tk.Label(self, text="Tamanho Total da Memória:")
        self.label_total_size.pack(pady=10)

        self.entry_total_size = tk.Entry(self, textvariable=self.total_size)
        self.entry_total_size.pack(pady=5)

        self.btn_iniciar = tk.Button(self, text="Iniciar", command=self.iniciar_segmentacao)
        self.btn_iniciar.pack(pady=10)

    def iniciar_segmentacao(self):
        try:
            total_size = self.total_size.get()
            if total_size <= 0:
                raise ValueError
            self.segmentacao = Segmentacao(total_size)
            self.abrir_painel_segmentacao()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido para a memória.")

    def abrir_painel_segmentacao(self):
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

            if self.segmentacao.alocar(process_id, tamanho):
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
        
        if self.segmentacao.desalocar(process_id):
            messagebox.showinfo("Sucesso", "Memória desalocada com sucesso.")
        else:
            messagebox.showwarning("Falha", "Falha ao desalocar memória.")
        self.display_memory()

    def limpar_memoria(self):
        self.segmentacao = Segmentacao(self.segmentacao.tamanho_total)
        messagebox.showinfo("Sucesso", "Memória limpa com sucesso.")
        self.display_memory()

    def display_memory(self):
        self.memory_canvas.delete("all")
        total_height = 400
        segment_height = total_height / self.segmentacao.tamanho_total

        for segment in self.segmentacao.memoria:
            y1 = segment.endereco_inicial * segment_height
            y2 = (segment.endereco_inicial + segment.tamanho) * segment_height

            if segment.id is None:
                fill_color = "lightblue"
                text = f"Segmento {segment.endereco_inicial}-{segment.endereco_inicial + segment.tamanho}: Livre"
            else:
                fill_color = "pink"
                text = f"Segmento {segment.endereco_inicial}-{segment.endereco_inicial + segment.tamanho}: Processo {segment.id}"

            self.memory_canvas.create_rectangle(0, y1, 800, y2, fill=fill_color)
            self.memory_canvas.create_text(400, (y1 + y2) / 2, text=text)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = InterfaceSegmentacao()
    app.mainloop()
