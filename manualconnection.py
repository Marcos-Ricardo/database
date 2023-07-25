
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os

class Connection():
    def __init__(self):
        self.login()

    def login(self):
        self.login_root = tk.Tk()
        self.login_root.geometry('380x160+410+200')
        self.login_root.configure(bg='#C0D9D9')
        
        tk.Label(self.login_root, text='Digite o seu usuário do seu banco de dados:', bg='#C0D9D9', fg='black').place(x=10, y=6)
        self.user = tk.Entry(self.login_root)
        self.user.place(x=250, y=6)

        tk.Label(self.login_root, text='Digite a senha do seu banco de dados:', bg='#C0D9D9', fg='black').place(x=10, y=35) 
        self.password = tk.Entry(self.login_root)
        self.password.place(x=250, y=35)

        tk.Label(self.login_root, text='Digite o host do seu banco de dados:', bg='#C0D9D9', fg='black').place(x=10, y=65)
        self.host = tk.Entry(self.login_root)
        self.host.place(x=250, y= 65)

        tk.Label(self.login_root, text='Digite qual banco de dados vai utilizar:', bg='#C0D9D9', fg='black').place(x=10, y=95)
        self.database = tk.Entry(self.login_root)
        self.database.place(x=250, y=95)

        tk.Button(self.login_root, text='ENVIAR', command=self.confirm_login).place(x=320, y=130)
        
        self.login_root.mainloop()
    def confirm_login(self):
        self.connection()
    
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
                self.login_root.destroy()
                self.screen()
                
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
        self.df = pd.DataFrame(self.response)
        self.query = 'SELECT * FROM clientes;'
        self.cursor.execute(self.query)
        self.response = self.cursor.fetchall()
        self.clear_screen_db()
        self.p_df.insert("1.0", self.df.to_string(index=False))
    
    def insert_data(self):
        self.screen()
        self.dataframe()
        self.p_df.insert("1.0", self.df.to_string(index=False))
        self.clear_screen()

    def clear_screen_db(self):
        self.p_df.delete("1.0", "end")
        
    def shutdown(self):
       self.mensagem =  messagebox.askquestion('MRTEC', 'Deseja mesmo encerrar o app?')
       if self.mensagem == 'yes':
           self.conn.close()
           self.cursor.close()
           os._exit(0)
           
           

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
                
    def insert_new_user_screnn(self):
        self.root_inserir = tk.Tk()
        self.root_inserir.geometry('340x180+405+30')
        self.root_inserir.configure(bg='grey')
        
        tk.Label(self.root_inserir, text='Insira o nome do usuário:', bg='grey').place(x=0.0, y=5)
        self.ist_name = tk.Entry(self.root_inserir)
        self.ist_name.place(x=180, y=5)

        tk.Label(self.root_inserir, text='Insira a idade do usuário:', bg='grey').place(x=0.0, y=35)
        self.ist_old = tk.Entry(self.root_inserir)
        self.ist_old.place(x=180, y=35)
        
        tk.Label(self.root_inserir, text='Insira a cidade do usuário:', bg='grey').place(x=0.0, y=65)
        self.ist_city = tk.Entry(self.root_inserir)
        self.ist_city.place(x=180, y=65)

        tk.Label(self.root_inserir, text='Insira a profissão do usuário:', bg='grey').place(x=0.0, y=95)
        self.ist_ocupation = tk.Entry(self.root_inserir)
        self.ist_ocupation.place(x=180, y=95)

        tk.Button(self.root_inserir, text='ENVIAR', command=self.save_new_user).place(x=250, y=130)
        
        self.root_inserir.mainloop()
       
    def screen(self):
        self.root = tk.Tk()
        self.root.title('MRTEC')
        self.root.geometry('663x470+300+50')
        self.root.config(bg='grey')
        
        tk.Button(self.root, text='MOSTRAR BANCO', command=self.show_dataframe).place(x=110, y=420)
        tk.Button(self.root, text='ENCERRAR', command=self.shutdown).place(x=587, y=420)
        tk.Button(self.root, text='INSERIR NOVO CLIENTE', command=self.insert_new_user_screnn).place(x=447, y=420)
        tk.Button(self.root, text='LIMPAR DADOS', command=self.clear_screen_db).place(x=10, y=420)

        self.p_df = tk.Text(self.root)
        self.p_df.place(x=10, y=10)

        self.root.mainloop()

Connection()

