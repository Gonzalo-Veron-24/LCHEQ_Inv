import numpy as np                               
import sympy
import openpyxl
import pandas as pd
import datetime

from sympy.core.symbol import Symbol


class LC():

    M_El = []
    M_No = []
    c_g_l = []
    d_g_d = []
    t_i = []
    j_i_d = []
    m_a = []
    m_g = []
    bt = {}
    m_b = []
    m_d = []
    k = []
    T_C_L = []
    m_e = []
    s_c = []
    D_e_o_t = []
    D_e_t = []

    def __init__(self, Ancho, Alto, Hx, Vy, D_e_E):
        self.Ancho = Ancho
        self.Alto = Alto
        self.Hx = Hx
        self.Vy = Vy
        self.D_e_E = D_e_E
        self.Area = (self.Ancho) * (self.Alto)
        self.AreaF = 4 * self.Area
        self.Xi = Symbol("xi")
        self.ita = Symbol("ita")
        self.N1,self.N2,self.N3,self.N4=(1/4)*(1-self.Xi)*(1-self.ita),(1/4)*(1+self.Xi)*(1-self.ita),(1/4)*(1+self.Xi)*(1+self.ita),(1/4)*(1-self.Xi)*(1+self.ita)
        self.Nodo_list=[self.N1,self.N2,self.N3,self.N4]
        

    def inicio(self):
        self.D_N = self.D_d_N()
        self.M_El = self.M_E()
        self.M_No = self.M_N()
        self.c_g_l = self.T_C()
        self.d_g_d = self.D_G()
        self.t_i = self.T_I()
        self.j_i_d = self.J_I_D()
        self.m_a = self.M_A()
        self.m_g = self.M_G()
        self.m_b = self.M_B()
        self.m_d = self.M_D()
        self.T_C_L=[x for x in range(1,(self.M_No.size*2)+1)]

    def validacion_float(ingreso):
        while True:
            valor = input(ingreso)
            try:
                valor=float(valor)
                return valor
            except:
                print("\n¡VALOR INGRESADO NO VALIDO!\n") 
    def D_d_N(self):
            DNL=[] #Lista de derivadas de los nodos
            for i in self.Nodo_list:
                dNdXi=i.diff(self.Xi)
                dNdita=i.diff(self.ita)
                DNL.append(dNdXi)
                DNL.append(dNdita)
            return DNL

    def M_E(self):
        M_elementos=[[x for x in range(1,self.Hx+1)]]
        for j in range(2, self.Vy+1):
            l_c=[]
            for i in range(M_elementos[-1][-1]+1, M_elementos[-1][-1]+self.Hx+1):
                l_c.append(i)
            M_elementos.append(l_c)
        M_elementos=np.array(M_elementos)
        return M_elementos

    def M_N(self):
        M_Nodos=[[x for x in range(1,self.Hx+2)]]
        for j in range(2, self.Vy+2):
            l_c=[]
            for i in range(M_Nodos[-1][-1]+1, M_Nodos[-1][-1]+self.Hx+2):
                l_c.append(i)
            M_Nodos.append(l_c)
        M_Nodos=np.array(M_Nodos)
        return M_Nodos

    def T_C(self):
        C_G_L={}
        for j in range(self.Vy):
            for i in range(self.Hx):
                C_G_L[self.M_El[j][i]]=[[self.M_No[j][i],self.M_No[j][i+1],self.M_No[j+1][i+1],self.M_No[j+1][i]],[(2*(self.M_No[j][i])-1),(2*(self.M_No[j][i])),(2*(self.M_No[j][i+1])-1),(2*(self.M_No[j][i+1])),(2*(self.M_No[j+1][i+1])-1),(2*(self.M_No[j+1][i+1])),(2*(self.M_No[j+1][i])-1),(2*(self.M_No[j+1][i]))]]
        return C_G_L

    def D_G(self):
        D_G_d = {}
        L_x = []
        L_y = []
        for j in range(1,self.Vy+1):
            for i in range(1,self.Hx+1):
                L_x.append([self.Ancho*(i-1),self.Ancho*i,self.Ancho*i,self.Ancho*(i-1)])
                L_y.append([self.Alto*(j-1),self.Alto*(j-1),self.Alto*j,self.Alto*j])
        for i in range(1,(self.Hx*self.Vy)+1):
            D_G_d[i]=[L_x[i-1],L_y[i-1]]
        return D_G_d

    def T_I(self):
        d = {}
        for i in self.d_g_d.keys():
            xf = (self.d_g_d[i][0][0])*(self.Nodo_list[0])+(self.d_g_d[i][0][1])*(self.Nodo_list[1])+(self.d_g_d[i][0][2])*(self.Nodo_list[2])+(self.d_g_d[i][0][3])*(self.Nodo_list[3])
            yf = (self.d_g_d[i][1][0])*(self.Nodo_list[0])+(self.d_g_d[i][1][1])*(self.Nodo_list[1])+(self.d_g_d[i][1][2])*(self.Nodo_list[2])+(self.d_g_d[i][1][3])*(self.Nodo_list[3])
            dXfdXi= xf.diff(self.Xi)
            dXfdita= xf.diff(self.ita)
            dYfdXi= yf.diff(self.Xi)
            dYfdita= yf.diff(self.ita)

            d[i] = [xf,yf,dXfdXi,dXfdita,dYfdXi,dYfdita]
        return d
    
    def J_I_D(self):
        j_i_d = {}
        for i in self.t_i.keys():
            J=np.array([[float(2*(self.t_i[i][2])),float(2*(self.t_i[i][4]))],[float(2*(self.t_i[i][3])),float(2*(self.t_i[i][5]))]])
            Inv_J=np.linalg.inv(J)
            Det_J = np.linalg.det(J)
            j_i_d[i]=[J,Inv_J,Det_J]
        return j_i_d

    def M_A(self):
        a = {}
        for i in self.j_i_d.keys():
            A = (1/self.j_i_d[i][2])*(np.array([[self.j_i_d[i][0][1,1],(-1)*(self.j_i_d[i][0][0,1]),0,0],[0,0,(-1)*(self.j_i_d[i][0][1,0]),self.j_i_d[i][0][0,0]],[(-1)*(self.j_i_d[i][0][1,0]),self.j_i_d[i][0][0,0],self.j_i_d[i][0][1,1],(-1)*(self.j_i_d[i][0][0,1])]]))
            a[i] = [A]
        return a

    def M_G(self):
        G=(1/4)*(np.array([[(-1)*(1-self.Vy),0,(1-self.Vy),0,(1+self.Vy),0,(-1)*(1+self.Vy),0],[(-1)*(1-self.Hx),0,(-1)*(1+self.Hx),0,(1+self.Hx),0,(1-self.Hx),0],[0,(-1)*(1-self.Vy),0,(1-self.Vy),0,(1+self.Vy),0,(-1)*(1+self.Vy)],[0,(-1)*(1-self.Hx),0,(-1)*(1+self.Hx),0,(1+self.Hx),0,(1-self.Hx)]]))
        return G

    def M_B(self):
        b = {}
        for i in self.m_a.keys():
            m = np.array(np.dot(self.m_a[i],self.m_g))
            b[i] = m[0]
            self.bt[i]= np.transpose(m[0])
        return b

    def M_D(self):
        matr_D= np.array([[self.D_e_E[2]/(1-self.D_e_E[4]*self.D_e_E[4]),self.D_e_E[4]*self.D_e_E[2]/(1-self.D_e_E[4]*self.D_e_E[4]),0],[self.D_e_E[4]*self.D_e_E[0]/(1-self.D_e_E[3]*self.D_e_E[3]),self.D_e_E[0]/(1-self.D_e_E[5]*self.D_e_E[3]),0],[0,0,(self.D_e_E[0]/(2*(1+self.D_e_E[3])))]])
        return matr_D

    def M_K(self, T):
        k = {}
        K = " "
        for t in self.m_b.keys():
            if t == 1:
                b_d=np.array(np.dot(self.m_d,self.m_b[t]))
                b_bt_d=np.array(np.dot(self.bt[t],b_d))
                M_p_k = []
                for j in range(8):
                    L_x = []
                    for i in range(8):
                        I_x = sympy.integrate(sympy.integrate(b_bt_d[i][j] , (self.Xi,-1,1)),(self.ita,-1,1))
                        L_x.append(float(I_x))
                    M_p_k.append(L_x)
                K = ((np.array(M_p_k))*(self.j_i_d[t][2])*T) 
            M_d_k = pd.DataFrame(list(zip(K[:,0],K[:,1],K[:,2],K[:,3],K[:,4],K[:,5],K[:,6],K[:,7])),self.c_g_l[t][1],self.c_g_l[t][1])
            M_O_K = (M_d_k.sort_index(axis=0)).sort_index(axis=1)
            k[t]= M_O_K
        return k

    def f_e_A(self,M1,M2):
        for e in M1.index:
            if(e==M2.index[e-1]):
                for i in M1.columns:
                    if(i==M2.columns[i-1]):
                        M2[e][i]+=M1[e][i]
    
    def f_e_B(self):
        Matriz_E=pd.DataFrame(list(zip()),self.T_C_L,self.T_C_L)
        Matriz_E=Matriz_E.fillna(0)
        for e in self.k.keys():
            self.f_e_A(self.k[e],Matriz_E)
        return Matriz_E

    def armado(self,Lista1,Lista2,dicc,e):#K,C_L,Ke,elemento
        Lista1c=Lista1.copy()
        for i in range(len(Lista1)): 
            Lista1c[i].insert(0,Lista2[e][i])
        Lista2[e].insert(0,'-')
        Lista1c.insert(0,Lista2[e])    
        dicc[e+1]=Lista1c
        return dicc

    def S_c_d(self,cant_c,Cargas): 
        for i in Cargas:
            self.s_c = self.S_C(i)
            M_e_n = np.array(self.m_e)
            M_e_ni = np.linalg.inv(M_e_n)
            Desplazamientos = pd.DataFrame(np.dot(M_e_ni,self.s_c),index=self.T_C_L)
            c_l = []
            for i in self.c_g_l.keys():
                for e in self.c_g_l[i][1]:
                    c_l.append(e)
            D_e_o = pd.DataFrame([0.0 for i in range(len(c_l))],index=c_l)
            for i in Desplazamientos.index:
                for e in D_e_o.index:
                    if i == e:
                        D_e_o[0][e] = Desplazamientos[0][e]

            #Su = 0
            #for e in range(1,(D_e_o.index[-1])+1):
            #    if (D_e_o.index[e-1])%2==0:
            #        Su+=abs(float(D_e_o[0][e]))

            #D_e = Su/(self.Alto*self.Vy)
            #(self.D_e_t).append(D_e)
            (self.D_e_o_t).append(D_e_o)
            

    def S_C(self,C):
        sist_c = (pd.DataFrame(list(zip()),self.T_C_L,[1])).fillna(0)
        CargaN = C/(2*len(self.M_No[0])-2)
        C_s=[]
        for j in range(0,-2,-1):
            lista = []
            for e in range(len(self.M_No[j])):
                if (e==0 or e==len(self.M_No[j])-1) and j==0:
                    lista.append(-CargaN)
                elif (e==0 or e==len(self.M_No[j])-1)==False and j==0:
                    lista.append(-2*CargaN)
                elif (e==0 or e==len(self.M_No[j])-1) and j==(-1):
                    lista.append(CargaN)
                elif (e==0 or e==len(self.M_No[j])-1)==False and j==(-1):
                    lista.append(2*CargaN)
            c_sc = pd.DataFrame(list(zip(lista)),2*self.M_No[j]-1,[1])
            C_s.append(c_sc)
        
        C_SCarga=pd.concat([C_s[0],C_s[1]])
        sist_c=(C_SCarga+sist_c).fillna(0)

        return sist_c




    def imprimir(self):
        for i in range(self.cant_c):
            print("\nDezplazamiento N°{}: \n{}".format((i+1),self.D_e_o_t[i]))
            #print("\nDeformacion equivalente N°{}: \n{}".format((i+1),self.D_e_t[i]))




