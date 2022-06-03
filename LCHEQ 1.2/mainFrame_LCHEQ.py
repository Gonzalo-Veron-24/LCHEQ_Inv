from tkinter import *
from tkinter import font
from typing import Sized
from tkinter.ttk import Combobox
from CLCH import LCH
from CLCM import LCM
from tkinter import messagebox




class MainFrame(Frame):

    Cargas = []
    N_C = 1

    def __init__(self, master=None):
        super().__init__(master, width=900, height=600)
        self.master = master
        self.pack()
        self.create_widgets()


    def D_y_C(self):
        try:
            self.Ancho = int(self.txtFn12.get())
            self.Alto = int(self.txtFn13.get())
            self.Hx = int(self.txtFn14.get())
            self.Vy = int(self.txtFn15.get())
            self.E1 = float(self.txtFn23.get())
            self.E2 = float(self.txtFn24.get())
            self.E3 = float(self.txtFn25.get())
            self.idc12 = float(self.txtFn26.get())
            self.idc13 = float(self.txtFn27.get())
            self.idc32 = float(self.txtFn28.get())
            self.L1 = float(self.txtFn29.get())
            self.F_A_i = float(self.txtFn210.get())
            self.Et = float(self.txtFn211.get())
            self.Ft = float(self.txtFn212.get())
            self.cant_c = int(self.txtFn213.get())

        except ValueError:
            messagebox.showerror(message = "ERROR DE TIPEO!", title="ALERTA")
            return 0
        except UnboundLocalError:
            messagebox.showerror(message = "CASILLAS SIN CARGA!", title="ALERTA")
            return 0
        self.T_L = self.Cmb.get()
        self.d_e_e = [self.E1,self.E2,self.E3,self.idc12,self.idc13,self.idc32,self.L1,self.F_A_i,self.Et,self.Ft]
        
        self.cargas(self.N_C)


    
    

    def d(self):
        try:
            c = float(self.winen.get())
            self.Cargas.append(c)
            self.N_C += 1
            self.win.destroy()
            if self.N_C <= self.cant_c:
                self.cargas(self.N_C)
            else:
                if self.T_L == "Ladrillo Hueco":
                    L_H = LCH(self.Ancho,self.Alto,self.Hx,self.Vy,self.d_e_e,1,self.cant_c,self.Cargas)
                    L_H.Guardado()
                elif self.T_L == "Ladrillo Macizo":
                    L_M = LCM(self.Ancho,self.Alto,self.Hx,self.Vy,self.d_e_e,1,self.cant_c,self.Cargas)

        except ValueError:
            messagebox.showerror(message = "ERROR DE TIPEO!", title="ALERTA")
            return 0
        except UnboundLocalError:
            messagebox.showerror(message = "CASILLAS SIN CARGA!", title="ALERTA")
            return 0

        
    def cargas(self, N_c):

        self.win = Toplevel()
        self.win.geometry("400x100")
        self.winlb = Label(self.win, text = "CARGA N°{}".format(N_c),font=("Arial",12))
        self.winlb.place(x=30,y=35,width=100)
        self.winen = Entry(self.win)
        self.winen.place(x=140, y=35,width=100,height=30)
        self.winbt = Button(self.win,text="ACEPTAR",font=("Arial",8), relief="raised", borderwidth=5,command=self.d)
        self.winbt.place(x=300,y=35,width=80,height=30)
        


    def create_widgets(self):
        Fn1 = Frame(self,width = 900, height=100 ,bg='#ECEDFC')
        Fn1.place(x=0, y=0)
        lbFn1 = Label(Fn1, text="Universidad Nacional de Misiones (UNAM)\nOBERA-MISIONES-ARGENTINA\nLCHEQ 1.1",bg='#ECEDFC',font=("Arial",15))
        lbFn1.place(x=150,y=15,width=600)

        Fn2 = Frame(self, width=900, height=150, bg='#ECEDFC')
        Fn2.place(x=0, y=100)
        lbFn2 = Label(Fn2,text="Dimensiones del objeto", font = ("Arial",15), bg='#ECEDFC')
        lbFn2.place(x=0,y=0,width=900,height=30)

        Fn21 = Frame(Fn2,width=430,height=45,bg='#ECEDFC')
        Fn21.place(x=10,y=40)
        lbFn12 = Label(Fn21,text="Ancho (mm)", font=("Arial",15),bg='#ECEDFC').place(x=100,y=5,width=150,height=35)
        self.txtFn12 = Entry(Fn21)
        self.txtFn12.place(x=270,y=5, width = 100,height = 35)

        Fn22 = Frame(Fn2,width=430,height=45,bg='#ECEDFC')
        Fn22.place(x=10,y=95)
        lbFn13 = Label(Fn22,text="Alto (mm)", font=("Arial",15),bg='#ECEDFC').place(x=100,y=5,width=150,height=35)
        self.txtFn13 = Entry(Fn22)
        self.txtFn13.place(x=270,y=5, width = 100,height = 35)

        Fn23 = Frame(Fn2,width=430,height=45,bg='#ECEDFC')
        Fn23.place(x=450,y=40)
        lbFn14 = Label(Fn23,text="Cantidad de elementos en X", font=("Arial",15),bg='#ECEDFC').place(x=25,y=5,width=270,height=35)
        self.txtFn14 = Entry(Fn23)
        self.txtFn14.place(x=310,y=5, width = 100,height = 35)

        Fn24 = Frame(Fn2,width=430,height=45,bg='#ECEDFC')
        Fn24.place(x=450,y=95)
        lbFn15 = Label(Fn24,text="Cantidad de elementos en Y", font=("Arial",15),bg='#ECEDFC').place(x=25,y=5,width=270,height=35)
        self.txtFn15 = Entry(Fn24)
        self.txtFn15.place(x=310,y=5, width = 100,height = 35)

        Fn3 = Frame(self, width=900, height=200, bg='#ECEDFC')
        Fn3.place(x=0, y=250)
        lbFn3 = Label(Fn3,text="Datos de ensayo y factores de ajuste", font = ("Arial",15), bg='#ECEDFC')
        lbFn3.place(x=0,y=0,width=900,height=30)

        Fn31 = Frame(Fn3,width=250,height=32.5,bg='#ECEDFC')
        Fn31.place(x=5,y=48.125)
        lbFn23 = Label(Fn31,text="Modulo Elastico (E1)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=120,height=31.5) 
        self.txtFn23 = Entry(Fn31)
        self.txtFn23.place(x=130,y=0.5, width = 115,height = 30)

        Fn32 = Frame(Fn3,width=250,height=32.5,bg='#ECEDFC')
        Fn32.place(x=5,y=98.75)
        lbFn24 = Label(Fn32,text="Modulo Elastico (E2)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=120,height=31.5) 
        self.txtFn24 = Entry(Fn32)
        self.txtFn24.place(x=130,y=0.5, width = 115,height = 30)

        Fn33 = Frame(Fn3,width=250,height=32.5,bg='#ECEDFC')
        Fn33.place(x=5,y=149.375)
        lbFn25 = Label(Fn33,text="Modulo Elastico (E3)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=120,height=31.5) 
        self.txtFn25 = Entry(Fn33)
        self.txtFn25.place(x=130,y=0.5, width = 115,height = 30)

        Fn311 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fn311.place(x=260,y=48.125)
        lbFn26 = Label(Fn311,text="Deformacion Correlativa (idc12)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn26 = Entry(Fn311)
        self.txtFn26.place(x=195,y=0.5, width = 100,height = 30)

        Fn322 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fn322.place(x=260,y=98.75)
        lbFn27 = Label(Fn322,text="Deformacion Correlativa (idc13)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn27 = Entry(Fn322)
        self.txtFn27.place(x=195,y=0.5, width = 100,height = 30)

        Fn333 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fn333.place(x=260,y=149.375)
        lbFn28 = Label(Fn333,text="Deformacion Correlativa (idc32)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn28 = Entry(Fn333)
        self.txtFn28.place(x=195,y=0.5, width = 100,height = 30)
        
        Fnb311 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fnb311.place(x=565,y=38)
        lbFn29 = Label(Fnb311,text="Valor promedio de ancho (L1)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn29 = Entry(Fnb311)
        self.txtFn29.place(x=195,y=0.5, width = 100,height = 30)

        Fnb322 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fnb322.place(x=565,y=78.5)
        lbFn210 = Label(Fnb322,text="Factor de Ajuste incremental (λ)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn210 = Entry(Fnb322)
        self.txtFn210.place(x=195,y=0.5, width = 100,height = 30)

        Fnb333 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fnb333.place(x=565,y=119)
        lbFn211 = Label(Fnb333,text="Modulo Tracción (Et)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn211 = Entry(Fnb333)
        self.txtFn211.place(x=195,y=0.5, width = 100,height = 30)

        Fnb334 = Frame(Fn3,width=300,height=32.5,bg='#ECEDFC')
        Fnb334.place(x=565,y=159.5)
        lbFn212 = Label(Fnb334,text="Resistencia Tracción (Ft)", font=("Arial",10),bg='#ECEDFC').place(x=5,y=0.5,width=190,height=31.5) 
        self.txtFn212 = Entry(Fnb334)
        self.txtFn212.place(x=195,y=0.5, width = 100,height = 30)

        Fn4 = Frame(self, width=900, height=150, bg='#ECEDFC')
        Fn4.place(x=0, y=450)
        lbFn4 = Label(Fn4,text="Estructuras regionales",font=("Arial",15),bg='#ECEDFC').place(x=50,y=20,width=200,height=70)

        self.E_r = ["Ladrillo Macizo","Ladrillo Hueco"]
        self.Cmb = Combobox(Fn4,width="10",values=self.E_r,state="readonly")
        self.Cmb.place(x=255,y=40,width=150,height=30)
        self.Cmb.current(0)

        lbFn213 = Label(Fn4,text="Cantidad de Ensayos", font=("Arial",14),bg='#ECEDFC').place(x=50,y=80,width=190,height=31.5) 
        self.txtFn213 = Entry(Fn4)
        self.txtFn213.place(x=275,y=80, width = 100,height = 30)

        self.btFn4 = Button(Fn4,text="INICIO",font=("Arial",20), relief="raised", borderwidth=5, command=self.D_y_C)
        self.btFn4.place(x=600,y=40,width=200,height=70)
        





