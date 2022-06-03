from Clase_LC_p import *


class LCM(LC):


    def __init__(self, Ancho, Alto, Hx, Vy, D_e_E, L1, cant_c, Cargas):
        super().__init__(Ancho, Alto, Hx, Vy, D_e_E)
        self.L1 = L1
        self.Cargas = Cargas
        self.T = 1
        (self.D_e_E).append(self.L1)
        (self.D_e_E).append(self.T)
        self.G12= float(self.D_e_E[0]/(2*(1+self.D_e_E[3])))
        self.D_e_E.append(self.G12)
        self.G13= float(self.D_e_E[0]/(2*(1+self.D_e_E[4])))
        self.D_e_E.append(self.G13)
        self.G23= float(self.D_e_E[1]/2/(1+self.D_e_E[5]))
        self.D_e_E.append(self.G23)
        self.cant_c = cant_c
        self.i_LCM()


    def i_LCM(self):
        self.inicio()
        self.k = self.M_K(self.T)
        self.m_e = self.f_e_B()
        self.S_c_d(self.cant_c,self.Cargas)