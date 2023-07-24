
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import messagebox

class Connection():
    def __init__(self):
        self.screen()

    def connection(self):
        user = self.user.get()
        password = self.password.get()
        host = self.host.get()
        database = self.database.get()
        if user and password and host and database != "":     
            self.dblogin = {'user': user,
                        'password': password,
                        'host': host,
                        'database': database    
                        }
            try:
                self.conn = mysql.connector.connect(**self.dblogin)
                self.cursor = self.conn.cursor()
                self.query = 'SELECT * FROM clientes;'
                self.cursor.execute(self.query)
                self.response = self.cursor.fetchall()
            except Exception as e:
                    self.clear_screen()
                    messagebox.showerror('ERRO', e)
        else:
            messagebox.showerror('MRTEC', 'Preencha todos os campos para prosseguir')       
    
    def clear_screen(self):
            self.user.delete(0, 'end')
            self.host.delete(0, 'end')
            self.database.delete(0, 'end')
            self.password.delete(0, 'end')

    def dataframe(self):
        self.connection()
        self.df = pd.DataFrame(self.response)

    def show_dataframe(self):
        self.p_df.insert("1.0", self.df.to_string(index=False))
        
    def insert_data(self):
        self.dataframe()
        self.p_df.insert("1.0", self.df.to_string(index=False))
        self.clear_screen()

    def clear_screen_db(self):
        self.p_df.delete("1.0", "end")
        
    def shutdown(self):
       self.mensagem =  messagebox.askquestion('MRTEC', 'Deseja mesmo encerrar o app?')
       if self.mensagem == 'yes':
           self.root.destroy()
           self.root_inserir.destroy()
           self.conn.close()
           self.cursor.close()

    def save_new_user(self):
            self.new_name = self.ist_name.get()
            self.new_old = self.ist_old.get()
            self.new_city = self.ist_city.get()
            self.new_ocupation = self.ist_ocupation.get()

            def insert_user():
                self.query = f"INSERT INTO clientes (nome, idade, cidade, profissao) VALUES ('{self.new_name}', '{self.new_old}', '{self.new_city}', '{self.new_ocupation}');"
                self.cursor.execute(self.query)
                self.conn.commit()
                         
            def clear_cad_screen():
                self.ist_name.delete(0, 'end')
                self.ist_old.delete(0, 'end')
                self.ist_city.delete(0, 'end')
                self.ist_ocupation.delete(0, 'end')
            if self.new_name and self.new_city and self.new_old and self.new_ocupation:
                self.confirm = messagebox.askquestion('MRTEC',f' Os dados digitados foram: \n{"Nome: ", self.new_name, "Idade: ",self.new_old, "Cidade: ",self.new_city, "Profissão: ",self.new_ocupation}')
                self.more_user_message = messagebox.askquestion('MRTEC', 'Continuar cadastrando?')
            else:
                messagebox.showerror('MRTEC', 'Preencha todos os campos solicitados')
                
            if self.more_user_message == 'yes':
                clear_cad_screen()
                insert_user()
            else:
                messagebox.showinfo('MRTEC', 'Dados salvos com sucesso')
                self.root_inserir.destroy()
                print(f'{"Nome: ",self.new_name}\n,{"Idade: ",self.new_old}\n, {"Cidade: ",self.new_city}\n, {"Profissão: ",self.new_ocupation}')
                insert_user()
                
    def inserir(self):
        self.root_inserir = tk.Tk()
        self.root_inserir.geometry('435x180')
        
        tk.Label(self.root_inserir, text='Insira o nome do usuário:').place(x=0.0, y=5)
        self.ist_name = tk.Entry(self.root_inserir)
        self.ist_name.pack(pady=5)

        tk.Label(self.root_inserir, text='Insira a idade do usuário:').place(x=0.0, y=35)
        self.ist_old = tk.Entry(self.root_inserir)
        self.ist_old.pack(pady=5)
        
        tk.Label(self.root_inserir, text='Insira a cidade do usuário:').place(x=0.0, y=65)
        self.ist_city = tk.Entry(self.root_inserir)
        self.ist_city.pack(pady=5)

        tk.Label(self.root_inserir, text='Insira a profissão do usuário:').place(x=0.0, y=95)
        self.ist_ocupation = tk.Entry(self.root_inserir)
        self.ist_ocupation.pack(pady=5)

        tk.Button(self.root_inserir, text='ENVIAR', command=self.save_new_user).place(x=250, y=130)
        
        self.root_inserir.mainloop()
       
    def screen(self):
        self.root = tk.Tk()
        self.root.title('MRTEC')
        self.root.geometry('690x620')
        self.root.config(bg='grey')
        
        tk.Label(self.root, text='Digite o seu usuário do seu banco de dados:', bg='grey').place(x=20, y=6)
        self.user = tk.Entry(self.root)
        self.user.pack(pady=5)

        tk.Label(self.root, text='Digite a senha do seu banco de dados:', bg='grey').place(x=20, y=35) 
        self.password = tk.Entry(self.root)
        self.password.pack(pady=5)

        tk.Label(self.root, text='Digite o host do seu banco de dados:', bg='grey').place(x=20, y=65)
        self.host = tk.Entry(self.root)
        self.host.pack(pady=5)

        tk.Label(self.root, text='Digite qual banco de dados vai utilizar:', bg='grey').place(x=20, y=95)
        self.database = tk.Entry(self.root)
        self.database.pack(pady=5)
        
        tk.Button(self.root, text='MOSTRAR BANCO', command=self.show_dataframe).place(x=23, y=130)
        tk.Button(self.root, text='ENVIAR', command=self.insert_data).place(x=348, y=130)
        tk.Button(self.root, text='ENCERRAR', command=self.shutdown).place(x=275, y=130)
        tk.Button(self.root, text='INSERIR NOVO CLIENTE', command=self.inserir).place(x=135, y=130)
        tk.Button(self.root, text='LIMPAR DADOS', command=self.clear_screen_db).place(x=403, y=130)

        self.p_df = tk.Text(self.root)
        self.p_df.pack(pady=50)

        self.root.mainloop()

Connection()

