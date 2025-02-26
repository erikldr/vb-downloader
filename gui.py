# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import downloader
import re

class Application:
    def __init__(self, master=None):
        self.root = master
        self.root.title("VB Downloader")
        self.config_file = "config.txt"
        self.pasta_destino = tk.StringVar(value="")
        self.prefixo_nome = tk.StringVar(value="audio")
        self.monitorando = [False]  # Usando uma lista para ser modificada dentro de threads
        self.thread_monitoramento = None

        self.load_config()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.create_destination_widgets()
        self.create_filename_widgets()
        self.create_control_buttons()

    def create_destination_widgets(self):
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(padx=10, pady=10)

        self.label_pasta = tk.Label(self.frame_principal, text="Pasta de Destino:")
        self.label_pasta.grid(row=0, column=0, sticky="w")

        self.entry_pasta = tk.Entry(self.frame_principal, textvariable=self.pasta_destino, width=40)
        self.entry_pasta.grid(row=1, column=0, padx=5, pady=5)

        self.botao_selecionar_pasta = tk.Button(self.frame_principal, text="...", command=self.selecionar_pasta)
        self.botao_selecionar_pasta.grid(row=1, column=1, padx=5)

        self.botao_abrir_pasta = tk.Button(self.frame_principal, text="Abrir Pasta", command=self.abrir_pasta)
        self.botao_abrir_pasta.grid(row=1, column=2, padx=5)

    def create_filename_widgets(self):
        self.label_nome = tk.Label(self.frame_principal, text="Nome do Arquivo:")
        self.label_nome.grid(row=2, column=0, sticky="w", pady=(10, 0))

        self.entry_nome = tk.Entry(self.frame_principal, textvariable=self.prefixo_nome, width=40)
        self.entry_nome.grid(row=3, column=0, padx=5, pady=5)

    def create_control_buttons(self):
        self.botao_iniciar = tk.Button(self.frame_principal, text="Iniciar Monitoramento", command=self.iniciar_monitoramento)
        self.botao_iniciar.grid(row=4, column=0, padx=5, pady=(10, 0), sticky='we')

        self.botao_parar = tk.Button(self.frame_principal, text="Parar Monitoramento", command=self.parar_monitoramento, state=tk.DISABLED)
        self.botao_parar.grid(row=4, column=1, padx=5, pady=(10, 0), sticky='we')

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_destino.set(pasta)

    def abrir_pasta(self):
        pasta = self.pasta_destino.get()
        if pasta and os.path.isdir(pasta):
            os.startfile(pasta) if os.name == 'nt' else os.system(f'xdg-open "{pasta}"')
        else:
            messagebox.showerror("Erro", "Pasta inválida ou não selecionada.")

    def iniciar_monitoramento(self):
        pasta = self.pasta_destino.get()
        prefixo = self.prefixo_nome.get()

        if not os.path.isdir(pasta):
          messagebox.showerror("Erro", "Selecione uma pasta valida")
          return

        if not re.fullmatch(r"^[a-zA-Z0-9_-]+$", prefixo):
          messagebox.showerror("Erro", "Nome do arquivo inválido. Use apenas letras, números, _ ou -.")
          return

        if self.monitorando[0]:
            messagebox.showinfo("Aviso", "O monitoramento já está em execução.")
            return

        self.monitorando = [True]
        self.botao_iniciar.config(text="Monitorando", state=tk.DISABLED)
        self.botao_parar.config(state=tk.NORMAL)

        self.thread_monitoramento = threading.Thread(target=self.executar_download_thread, args=(pasta, prefixo, self.monitorando))
        self.thread_monitoramento.daemon = True
        self.thread_monitoramento.start()

    def executar_download_thread(self, pasta, prefixo, monitorando):
        terminou_por_tempo = [False]
        downloader.executar_download(pasta, prefixo, terminou_por_tempo, monitorando)
        self.monitorando[0] = False
        self.botao_iniciar.config(text="Iniciar Monitoramento", state=tk.NORMAL)
        self.botao_parar.config(state=tk.DISABLED)

        if terminou_por_tempo[0]:
            messagebox.showinfo("Aviso", "Tempo limite atingido (20:58). O processo será encerrado até o próximo dia útil.")

    def parar_monitoramento(self):
        if self.monitorando[0]:
            print("Parando o monitoramento...")
            self.monitorando[0] = False
            self.botao_parar.config(state=tk.DISABLED)
            self.botao_iniciar.config(state=tk.NORMAL, text="Iniciar Monitoramento")

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                for line in f:
                    key, value = line.strip().split("=")
                    if key == "pasta_destino":
                        self.pasta_destino.set(value)
                    elif key == "prefixo_nome":
                        if value:
                            self.prefixo_nome.set(value)
                        else:
                            self.prefixo_nome.set(downloader.PREFIXO_PADRAO)
        except FileNotFoundError:
            print("Arquivo de configuração não encontrado. Usando valores padrão.")
        except ValueError:
            print("Arquivo de configuração corrompido. Usando valores padrão.")

    def save_config(self):
        with open(self.config_file, "w") as f:
            f.write(f"pasta_destino={self.pasta_destino.get()}\n")
            f.write(f"prefixo_nome={self.prefixo_nome.get()}\n")

    def on_closing(self):
        self.save_config()
        self.root.destroy()

root = tk.Tk()
Application(root)
root.mainloop()
