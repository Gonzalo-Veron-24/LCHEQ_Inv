from Clase_LC_p import *



class LCH(LC):


    def __init__(self, Ancho, Alto, Hx, Vy, D_e_E, L1, cant_c, Cargas):
        super().__init__(Ancho, Alto, Hx, Vy, D_e_E)
        self.L1 = L1
        self.Cargas=Cargas
        self.T = (self.D_e_E[7]/(self.D_e_E[9]/self.D_e_E[8]))*self.D_e_E[6]
        (self.D_e_E).append(self.L1)
        (self.D_e_E).append(self.T)
        self.G12= float(self.D_e_E[0]/(2*(1+self.D_e_E[3])))
        self.D_e_E.append(self.G12)
        self.G13= float(self.D_e_E[0]/(2*(1+self.D_e_E[4])))
        self.D_e_E.append(self.G13)
        self.G23= float(self.D_e_E[1]/2/(1+self.D_e_E[5]))
        self.D_e_E.append(self.G23)
        self.cant_c = cant_c
        self.i_LCH()

    def Guardado(self):
        T_de_M=datetime.datetime.now()
        T_de_Mstr=str(T_de_M.day)+"-"+str(T_de_M.month)+"-"+str(T_de_M.year)+" "+str(T_de_M.hour)+";"+str(T_de_M.minute)+";"+str(T_de_M.second)
        H_Excel=pd.ExcelWriter(T_de_Mstr+".xlsx")


        for i in range(self.cant_c):
            self.D_e_o_t[i].to_excel(H_Excel,sheet_name="{}".format(self.Cargas[i]))
            self.D_e_o_t[i].to_csv('Desplazamientos.csv')
            H_Excel.save()

    def i_LCH(self):
        self.inicio()
        self.k = self.M_K(self.T)
        self.m_e = self.f_e_B()
        self.S_c_d(self.cant_c,self.Cargas)


