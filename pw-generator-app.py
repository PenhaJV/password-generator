import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import random

class App:
    def __init__(self, root):
        # Inicialização da aplicação
        self.root = root
        self.root.title("Gerador de Senhas")

        # Instância da classe ListaAtualizavel
        self.lista_atualizavel = ListaAtualizavel()

        # Listbox para exibir as senhas geradas
        self.listbox = tk.Listbox(root)
        self.listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Atualiza a lista exibida na Listbox
        self.atualizar_lista()

        # Combobox para seleção de opções
        opcoes = ["COMPUTADOR", "CELULAR", "BANCO", "OUTRA OPÇÃO"]
        self.combobox = ttk.Combobox(root, width=20, values=opcoes)
        self.combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.combobox.bind("<<ComboboxSelected>>", self.atualizar_entrada_usuario)
        
        # Outra Opção
        self.outra_opcao_label = tk.Label(root, text="Outra Opção:", font=('TkFixedFont', 12))
        self.outra_opcao_entry = tk.Entry(root, width=10, font=('TkFixedFont', 12))
        self.outra_opcao_label.grid_forget()
        self.outra_opcao_entry.grid_forget()
        
        # Banco
        self.nome_banco_label = tk.Label(root, text="Nome do banco:", font=('TkFixedFont', 12))
        self.nome_banco_entry = tk.Entry(root, width=10,  font=('TkFixedFont', 12))
        self.nome_banco_label.grid_forget()
        self.nome_banco_entry.grid_forget()

        # Checkbuttons para escolher tipos de caracteres na senha
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
        tamanho_label.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.tamanho_entry = tk.Entry(root, width=5)
        self.tamanho_entry.grid(row=4, column=1, padx=10, pady=10)

        # Botões para gerar e excluir senhas
        gerar_senha_button = tk.Button(root, text="Gerar", command=self.gerar_senha)
        gerar_senha_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        excluir_senha_button = tk.Button(root, text="Excluir", command=self.remover_item)
        excluir_senha_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Configura o layout da grade para se expandir
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
            root.grid_rowconfigure(0, weight=1)

        # Fonte Monospace Tamanho 12
        self.root.option_add('*Font', 'TkFixedFont 12')

    def atualizar_lista(self):
        # Atualiza a Listbox com os itens da lista atualizável
        self.listbox.delete(0, tk.END)
        for item in self.lista_atualizavel.lista:
            self.listbox.insert(tk.END, item)

    def atualizar_entrada_usuario(self, event):
        # Atualiza os campos de entrada com base na opção selecionada
        opcao_selecionada = self.combobox.get()
        if opcao_selecionada == "OUTRA OPÇÃO":
            self.outra_opcao_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
            self.outra_opcao_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
            self.nome_banco_label.grid_forget()
            self.nome_banco_entry.grid_forget()
            
        elif opcao_selecionada == "BANCO":
            self.nome_banco_label.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
            self.nome_banco_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
            self.outra_opcao_label.grid_forget()
            self.outra_opcao_entry.grid_forget()
          
        else:
            self.nome_banco_label.grid_forget()
            self.nome_banco_entry.grid_forget()
            self.outra_opcao_label.grid_forget()
            self.outra_opcao_entry.grid_forget()
            
    def gerar_senha(self):
        # Gera uma senha com base nas opções escolhidas
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
            caracteres += ''.join(char for char in string.punctuation if char not in "~\"'()/:<=>[\\]^_`{|}")

        tamanho_senha = int(self.tamanho_entry.get()) if self.tamanho_entry.get().isdigit() else 12
        senha_gerada = ''.join(random.choice(caracteres) for _ in range(tamanho_senha))

        if opcao_selecionada == "BANCO":
            senha_gerada = f"BANCO ({entrada_usuario}) -> {senha_gerada}"
        elif opcao_selecionada == "OUTRA OPÇÃO":
            senha_gerada = f"{self.outra_opcao_entry.get().upper()} -> {senha_gerada}"
        else:
            senha_gerada = f"{opcao_selecionada} -> {senha_gerada}"

        novo_item = senha_gerada
        self.lista_atualizavel.adicionar_item(novo_item)
        self.atualizar_lista()

    def remover_item(self):
        # Remove o item selecionado da Listbox e da lista atualizável
        selecionado = self.listbox.curselection()
        if selecionado:
            item = self.listbox.get(selecionado[0])
            self.lista_atualizavel.remover_item(item)
            self.atualizar_lista()
        else:
            messagebox.showwarning("Aviso", "Selecione uma senha para remover.")

class ListaAtualizavel:
    def __init__(self):
        # Inicializa a lista e carrega os dados do arquivo, se existir
        self.lista = self.carregar_lista()

    def carregar_lista(self):
        # Carrega os itens da lista a partir do arquivo
        try:
            with open("lista.txt", "r") as arquivo:
                return [linha.strip() for linha in arquivo.readlines()]
        except FileNotFoundError:
            return []

    def salvar_lista(self):
        # Salva a lista no arquivo
        with open("lista.txt", "w") as arquivo:
            for item in self.lista:
                arquivo.write(item + "\n")

    def adicionar_item(self, item):
        # Adiciona um item à lista, salva no arquivo e realiza backup
        self.lista.append(item)
        self.salvar_lista()
        self.realizar_backup()

    def remover_item(self, item):
        # Remove um item da lista e salva no arquivo
        if item in self.lista:
            self.lista.remove(item)
            self.salvar_lista()

    def realizar_backup(self):
        # Realiza backup da lista
        backup_lista = self.lista.copy()
        backup_path = ".backup"
        with open(backup_path, "w") as backup_arquivo:
            for item in backup_lista:
                backup_arquivo.write(item + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
