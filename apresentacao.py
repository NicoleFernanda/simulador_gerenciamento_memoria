import tkinter as tk

from interfaces.interface_dinamica import InterfaceDinamica
from interfaces.interface_estatica_relocavel import InterfaceEstatica
from interfaces.interface_paginacao import InterfacePaginacao
from interfaces.interface_segmentacao import InterfaceSegmentacao

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Memória")
        self.geometry("300x200")
        self.center_window(300, 200)
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.label_selecao = tk.Label(self, text="Selecione o tipo de Gerenciamento de Memória:")
        self.label_selecao.pack(pady=10)

        self.btn_dinamica = tk.Button(self, text="Alocação Particionada Dinâmica", command=self.abrir_dinamica)
        self.btn_dinamica.pack(pady=5)

        self.btn_estatica = tk.Button(self, text="Alocação Particionada Estática Relocável", command=self.abrir_estatica)
        self.btn_estatica.pack(pady=5)

        self.btn_paginacao = tk.Button(self, text="Paginação", command=self.abrir_paginacao)
        self.btn_paginacao.pack(pady=5)

        self.btn_segmentacao = tk.Button(self, text="Segmentação", command=self.abrir_segmentacao)
        self.btn_segmentacao.pack(pady=5)

    def abrir_dinamica(self):
        self.destroy()
        app = InterfaceDinamica()
        app.mainloop()

    def abrir_estatica(self):
        self.destroy()
        app = InterfaceEstatica()
        app.mainloop()

    def abrir_paginacao(self):
        self.destroy()
        app = InterfacePaginacao()
        app.mainloop()

    def abrir_segmentacao(self):
        self.destroy()
        app = InterfaceSegmentacao()
        app.mainloop()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()