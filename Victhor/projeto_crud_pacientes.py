import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import time

# Conectar ao banco de dados
conn = sqlite3.connect("clinica.db")
c = conn.cursor()

# Criar tabela se não existir (alterada para incluir os novos campos)
c.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    data_nascimento TEXT,
    cpf TEXT,
    email TEXT,
    tipo_sanguineo TEXT,
    alergia TEXT,
    historico TEXT
)
''')
conn.commit()


def salvar_dados():
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    tipo_sanguineo = entry_tipo_sanguineo.get()
    alergia = entry_alergia.get()
    historico = entry_historico.get()

    if nome and data_nascimento and cpf and email and tipo_sanguineo and alergia and historico:
        c.execute('''
        INSERT INTO pacientes (nome, data_nascimento, cpf, email, tipo_sanguineo, alergia, historico)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, data_nascimento, cpf, email, tipo_sanguineo, alergia, historico))
        conn.commit()
        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
        # Limpar os campos do formulário
        entry_nome.delete(0, tk.END)
        entry_data_nascimento.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_tipo_sanguineo.delete(0, tk.END)
        entry_alergia.delete(0, tk.END)
        entry_historico.delete(0, tk.END)
        listar_pacientes()
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")


def listar_pacientes():
    for widget in frame_lista.winfo_children():
        widget.destroy()
    c.execute("SELECT * FROM pacientes")
    pacientes = c.fetchall()
    for paciente in pacientes:
        frame = tk.Frame(frame_lista, bg="white")
        frame.pack(fill="x")
        tk.Label(frame,
                 text=f"ID: {paciente[0]} - Nome: {paciente[1]} - Nascimento: {paciente[2]} - CPF: {paciente[3]} - Email: {paciente[4]} - Tipo Sanguíneo: {paciente[5]} - Alergia: {paciente[6]} - Histórico: {paciente[7]}",
                 bg="white").pack(side="left")
        tk.Button(frame, text="Editar", command=lambda pid=paciente[0]: editar_paciente(pid)).pack(side="right")
        tk.Button(frame, text="Excluir", command=lambda pid=paciente[0]: excluir_paciente(pid)).pack(side="right")


def excluir_paciente(paciente_id):
    c.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Paciente excluído!")
    listar_pacientes()


def editar_paciente(paciente_id):
    global entry_nome, entry_data_nascimento, entry_cpf, entry_email, entry_tipo_sanguineo, entry_alergia, entry_historico, btn_enviar
    c.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = c.fetchone()
    if paciente:
        entry_nome.delete(0, tk.END)
        entry_data_nascimento.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_tipo_sanguineo.delete(0, tk.END)
        entry_alergia.delete(0, tk.END)
        entry_historico.delete(0, tk.END)

        entry_nome.insert(0, paciente[1])
        entry_data_nascimento.insert(0, paciente[2])
        entry_cpf.insert(0, paciente[3])
        entry_email.insert(0, paciente[4])
        entry_tipo_sanguineo.insert(0, paciente[5])
        entry_alergia.insert(0, paciente[6])
        entry_historico.insert(0, paciente[7])

        btn_enviar.config(text="Atualizar", command=lambda: atualizar_paciente(paciente_id))


def atualizar_paciente(paciente_id):
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    tipo_sanguineo = entry_tipo_sanguineo.get()
    alergia = entry_alergia.get()
    historico = entry_historico.get()

    if nome and data_nascimento and cpf and email and tipo_sanguineo and alergia and historico:
        c.execute('''
        UPDATE pacientes
        SET nome=?, data_nascimento=?, cpf=?, email=?, tipo_sanguineo=?, alergia=?, historico=?
        WHERE id=?
        ''', (nome, data_nascimento, cpf, email, tipo_sanguineo, alergia, historico, paciente_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_data_nascimento.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_tipo_sanguineo.delete(0, tk.END)
        entry_alergia.delete(0, tk.END)
        entry_historico.delete(0, tk.END)
        btn_enviar.config(text="Salvar", command=salvar_dados)
        listar_pacientes()
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")


def alternar_tema():
    if root.cget("bg") == "white":
        root.config(bg="black")
        frame_lista.config(bg="black")
        btn_tema.config(bg="gray", fg="white", text="Modo Claro")
        btn_enviar.config(bg="gray", fg="white")
        for widget in root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry)):
                widget.config(bg="black", fg="white", insertbackground="white", highlightbackground="black")
    else:
        root.config(bg="white")
        frame_lista.config(bg="white")
        btn_tema.config(bg="SystemButtonFace", fg="black", text="Modo Escuro")
        btn_enviar.config(bg="SystemButtonFace", fg="black")
        for widget in root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry)):
                widget.config(bg="white", fg="black", insertbackground="black", highlightbackground="white")


# Tela de carregamento
def splash_screen():
    splash = tk.Toplevel()
    splash.geometry("400x300")
    splash.title("Carregando...")
    splash.configure(bg="white")
    imagem_original = Image.open("logo.png")
    imagem_redimensionada = imagem_original.resize((200, 200))
    imagem = ImageTk.PhotoImage(imagem_redimensionada)
    tk.Label(splash, image=imagem, bg="white").pack(expand=True)
    splash.update()
    time.sleep(2)
    splash.destroy()
    splash.imagem = imagem


# Início do programa
root = tk.Tk()
root.withdraw()
splash_screen()
root.deiconify()

root.title("Cadastro de Pacientes")
root.geometry("400x600")
root.config(bg="white")

# Adicionando os novos campos
label_nome = tk.Label(root, text="Nome", bg="white")
label_nome.pack()
entry_nome = tk.Entry(root, bg="white")
entry_nome.pack()

label_data_nascimento = tk.Label(root, text="Data de Nascimento", bg="white")
label_data_nascimento.pack()
entry_data_nascimento = tk.Entry(root, bg="white")
entry_data_nascimento.pack()

label_cpf = tk.Label(root, text="CPF", bg="white")
label_cpf.pack()
entry_cpf = tk.Entry(root, bg="white")
entry_cpf.pack()

label_email = tk.Label(root, text="Email", bg="white")
label_email.pack()
entry_email = tk.Entry(root, bg="white")
entry_email.pack()

label_tipo_sanguineo = tk.Label(root, text="Tipo Sanguíneo", bg="white")
label_tipo_sanguineo.pack()
entry_tipo_sanguineo = tk.Entry(root, bg="white")
entry_tipo_sanguineo.pack()

label_alergia = tk.Label(root, text="Alergia", bg="white")
label_alergia.pack()
entry_alergia = tk.Entry(root, bg="white")
entry_alergia.pack()

label_historico = tk.Label(root, text="Histórico", bg="white")
label_historico.pack()
entry_historico = tk.Entry(root, bg="white")
entry_historico.pack()

btn_enviar = tk.Button(root, text="Salvar", command=salvar_dados)
btn_enviar.pack(pady=10)

btn_tema = tk.Button(root, text="Modo Escuro", command=alternar_tema)
btn_tema.place(relx=1.0, rely=0.0, anchor="ne")

frame_lista = tk.Frame(root, bg="white")
frame_lista.pack()
listar_pacientes()

root.mainloop()
