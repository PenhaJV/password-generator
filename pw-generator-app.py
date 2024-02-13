import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import random

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Senhas")

        self.lista_atualizavel = ListaAtualizavel()

        # Listbox
        self.listbox = tk.Listbox(root)
        self.listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.atualizar_lista()

        # Combobox
        opcoes = ["COMPUTADOR", "CELULAR", "BANCO", "OUTRA OPÇÃO"]
        self.combobox = ttk.Combobox(root, width=10, values=opcoes)
        self.combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.combobox.bind("<<ComboboxSelected>>", self.atualizar_entrada_usuario)

        # Checkbuttons
        self.letras_var = tk.IntVar()
        self.letras_checkbox = tk.Checkbutton(root, text="aBc", variable=self.letras_var)
        self.letras_checkbox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.numeros_var = tk.IntVar()
        self.numeros_checkbox = tk.Checkbutton(root, text="123", variable=self.numeros_var)
        self.numeros_checkbox.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.caracteres_var = tk.IntVar()
        self.caracteres_checkbox = tk.Checkbutton(root, text="&#$", variable=self.caracteres_var)
        self.caracteres_checkbox.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        # Tamanho da Senha
        tamanho_label = tk.Label(root, text="Tamanho da senha:")
        tamanho_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.tamanho_entry = tk.Entry(root, width=5)
        self.tamanho_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botões
        gerar_senha_button = tk.Button(root, text="Gerar", command=self.gerar_senha)
        gerar_senha_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        excluir_senha_button = tk.Button(root, text="Excluir", command=self.remover_item)
        excluir_senha_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Configurar o layout da grade para se expandir
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Fonte Monospace Tamanho 12
        self.root.option_add('*Font', 'TkFixedFont 12')

    def atualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for item in self.lista_atualizavel.lista:
            self.listbox.insert(tk.END, item)


# ATUALIZAR ENTRADA PARA BANCO COM .ENTRY.GET()
    def atualizar_entrada_usuario(self, event):
        opcao_selecionada = self.combobox.get()
        if opcao_selecionada == "BANCO":
            self.nome_banco_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")
            self.nome_banco_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        else:
            self.nome_banco_label.grid_forget()
            self.nome_banco_entry.grid_forget()

    def gerar_senha(self):
        opcao_selecionada = self.combobox.get()
        entrada_usuario = self.nome_banco_entry.get() if opcao_selecionada == "BANCO" else opcao_selecionada

        if not entrada_usuario:
            messagebox.showwarning("Aviso", "Selecione uma opção válida para gerar senha.")
            return

        caracteres = ""
        if self.letras_var.get():
            caracteres += string.ascii_letters
        if self.numeros_var.get():
            caracteres += string.digits
        if self.caracteres_var.get():
            # Remover caracteres rejeitados
            caracteres += ''.join(char for char in string.punctuation if char not in "~\"'()/:<=>[\\]^_`{|}")

        tamanho_senha = int(self.tamanho_entry.get()) if self.tamanho_entry.get().isdigit() else 12
        senha_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho_senha))

        if opcao_selecionada == "BANCO":
            senha_gerada = f"BANCO ({entrada_usuario}) - {senha_gerada}"
        else:
            senha_gerada = f"{opcao_selecionada} - {senha_gerada}"

        novo_item = senha_gerada
        self.lista_atualizavel.adicionar_item(novo_item)
        self.atualizar_lista()

    def remover_item(self):
        selecionado = self.listbox.curselection()
        if selecionado:
            item = self.listbox.get(selecionado[0])
            self.lista_atualizavel.remover_item(item)
            self.atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Selecione uma senha para remover.")

class ListaAtualizavel:
    def __init__(self):
        self.lista = self.carregar_lista()

    def carregar_lista(self):
        try:
            with open("arquivos/lista.txt", "r") as arquivo:
                return [linha.strip() for linha in arquivo.readlines()]
        except FileNotFoundError:
            return []

    def salvar_lista(self):
        with open("arquivos/lista.txt", "w") as arquivo:
            for item in self.lista:
                arquivo.write(item + "\n")

    def adicionar_item(self, item):
        self.lista.append(item)
        self.salvar_lista()
        self.realizar_backup()

    def remover_item(self, item):
        if item in self.lista:
            self.lista.remove(item)
            self.salvar_lista()

    def realizar_backup(self):
        backup_lista = self.lista.copy()
        backup_path = "arquivos/.backup"
        with open(backup_path, "w") as backup_arquivo:
            for item in backup_lista:
                backup_arquivo.write(item + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

