# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 18:46:42 2021

@author: unam
"""
#Librerias-------------------------------------------------------------------------
import numpy as np                               
from numpy import matrix 
from sympy import Symbol
import openpyxl
import pandas as pd
import datetime
from sympy.core.facts import deduce_alpha_implications
from tqdm.auto import tqdm
import C_F #Codigo de funciones

# from colorama import init, Fore, Back, Style

##SE IMPORTAN LAS LIBRERIAS NECESARIAS PARA REALIZAR EL PROGRAMA

#PRESENTACION-------------------------------------------------------------------
print('¡Bienvenido! Por favor siga las instrucciones'.center(100))
print('Universidad Nacional de Misiones (UNAM)'.center(100))
print('Facultad de Ingeniería'.center(100))
print('OBERÁ-MISIONES/ARGENTINA'.center(100))

##AYUDA MEMORIA DE LOS DATOS
##ACLARAR DISPOSICION DE ELEMENTO PARA IDENTIFICAR CORRECTAMENTE EL ALTO Y EL ANCHO!!!
#Base de datos------------------------------------------------------------------

CLL=[-1,-1,-1,1,1,1,1,-1] #Cordenadas Locales Lista

print('\nCoordenadas locales establecidas en sentido horario: {}\n'.format(CLL))

#SE PIEDEN INGRESO DE DATOS DEL ELEMENTO FINITO
print('Ingrese las dimensiones del objeto'.center(100))  

Ancho=C_F.validacion_float('* Ancho(mm): ')
Alto=C_F.validacion_float('* Alto(mm): ')
Area=float(Alto*Ancho)
print('* Area: {}'.format(Area))

AreaF=float((CLL[4]-CLL[0])*(CLL[5]-CLL[1])*Area)  # (1-(-1))*(1-(-1))*Area

print('* Area del elemento finito: {}'.format(AreaF))

Hx=int(C_F.validacion_float('\nIngrese la cantidad de elementos en X: '))
Vy=int(C_F.validacion_float('Ingrese la cantidad de elementos en Y: '))

#Datos de ensayo
print()
print('Ingrese los datos de ensayo y factores de ajuste'.center(100)) 
D_d_E=[]
for i in range(2):
    for e in range(1,4):
        if i==0:
            D_d_E.append(C_F.validacion_float("* Modulo Elástico (E{}): ".format(e)))
        else:
            if e==1 or e==2:
                D_d_E.append(C_F.validacion_float('* Deformacion Correlativa, idc{}{}: '.format(1,e+1)))
            else:
                D_d_E.append(C_F.validacion_float('* Deformacion Correlativa, idc{}{}: '.format(e,e-1)))
    print()
D_d_E.append(C_F.validacion_float('\n* Factor de Ajuste exponencial (C): '))
D_d_E.append(C_F.validacion_float('* Factor de Ajuste incremental (K): '))

L1= 1                              
D_d_E.append(L1)
#espesor equivalente
T=(D_d_E[7]*Ancho)**D_d_E[6]                  #EN INVESTIGACIÓN... 
D_d_E.append(T)   

G12= float(D_d_E[0]/(2*(1+D_d_E[3])))
D_d_E.append(G12)
G13= float(D_d_E[0]/(2*(1+D_d_E[4])))
D_d_E.append(G13)
G23= float(D_d_E[1]/2/(1+D_d_E[5]))
D_d_E.append(G23)

print("\nEL ALGORITMO ESTA INICIANDO LOS CALCULOS CORRESPONDIENTES")
for i in tqdm(range(4000)):
    print("", end='\r')

#FORMACION DE MATRIZ K elemetal----------------------------------------------------------

print(D_d_E)
#Funciones de forma
Xi = Symbol("Xi")  
ita = Symbol("ita")  
N1=(1/4)*(1-Xi)*(1-ita)
N2=(1/4)*(1-Xi)*(1+ita)
N3=(1/4)*(1+Xi)*(1+ita)
N4=(1/4)*(1+Xi)*(1-ita)

Nodo_list=[N1,N2,N3,N4]

#Derivadas Parciales
DNL=[] #Derivadas de nodos lista
for i in Nodo_list:
    dNdXi= i.diff(Xi)
    DNL.append(dNdXi)
    dNdita= i.diff(ita)
    DNL.append(dNdXi)


Xf= (N1*CLL[0])+(N2*CLL[2])+(N3*CLL[4])+(N4*CLL[6])   
Yf= (N1*CLL[1])+(N2*CLL[3])+(N3*CLL[5])+(N4*CLL[7])

dXfdXi= Xf.diff(Xi)
dXfdita= Xf.diff(ita)
dYfdXi= Yf.diff(Xi)
dYfdita= Yf.diff(ita)


#Matriz Jacobiana------------------------------------------------------------------
#J= matrix([[dXfdXi,dYfdXi],
#           [dXfdita,dYfdita]])

Jacobianos=[]
Inv=[]
M_b=[] #Matriz B, listas
Lista_B=[]
for i in range(4):

    J=matrix([[float(dXfdXi.subs(ita,CLL[i*2])),float(dYfdXi.subs(ita,CLL[(i*2)+1]))],[float(dXfdita.subs(Xi,CLL[(i*2)])),float(dYfdita.subs(Xi,CLL[(i*2)+1]))]]) #Jacobianos

    Inv_J=np.array(np.linalg.inv(J)) #Inversas

    CdNdXi= Nodo_list[i].subs(ita,CLL[(i*2)+1]).diff(Xi)
    CdNdita= Nodo_list[i].subs(Xi,CLL[(i*2)]).diff(ita)
    
    b=[[float(CdNdXi*(float(Inv_J[0,0]))+CdNdita*(float(Inv_J[1,0]))),float(0)],
           [float(0),float(CdNdXi*(float(Inv_J[0,1]))+CdNdita*(float(Inv_J[1,1])))],
           [float(CdNdXi*(float(Inv_J[0,1]))+CdNdita*(float(Inv_J[1,1]))),float(CdNdXi*(float(Inv_J[0,0]))+CdNdita*(float(Inv_J[1,0])))]] #Matrices B
    
    if i==0:
        Lista_B.append(b[0])  #primero le agrego a la lista las componentes de la primera matriz b
        Lista_B.append(b[1])  # luego, cuando i toma valores distintos de cero
        Lista_B.append(b[2])  # le sumamos a cada indice de la lista los terminos especificos
        #de la matiz posterior. Por ultimo de esa lista creamos la matriz con array

    else:
        for e in range(3):
            Lista_B[e]=Lista_B[e]+b[e]

    bn=np.array(b) #Se creo la matriz mediante el metodo array de numpy
    #este nos facilita manipular la matriz

    Jacobianos.append(J)
    Inv.append(Inv_J)
    M_b.append(bn)

    print('\nJacobiano N°{}:\n{}'.format(i+1,J))
    print('Inversa del Jacobiano N°{}:\n{}'.format(i+1,J))
    print('Matriz B N°{}:\n{}'.format(i+1,bn))

# print(M_b[0][0,:])
B=np.array(Lista_B)
print('Matriz B:\n{}'.format(B))
Bt=np.transpose(B)
print('\nMatriz transpuesta de B:\n{}'.format(Bt))


list_D= [[D_d_E[2]/(1-D_d_E[4]*D_d_E[4]),D_d_E[4]*D_d_E[2]/(1-D_d_E[4]*D_d_E[4]),0],[D_d_E[4]*D_d_E[0]/(1-D_d_E[3]*D_d_E[3]),D_d_E[0]/(1-D_d_E[5]*D_d_E[3]),0],[0,0,D_d_E[11]]]
matr_D= np.array(list_D)
print("\nMatriz D")
print(matr_D) #Consultar si esta bien la formacion de esta matriz/ diferenciar entre el de LCHEQ2 y LCHEQ3 por que generan disparidad de datos

# a=D_d_E[2]/(1-D_d_E[4]*D_d_E[4])
# b=D_d_E[4]*D_d_E[2]*(1-D_d_E[4]*D_d_E[4])
# d=D_d_E[4]*D_d_E[0]/(1-D_d_E[3]*D_d_E[3])
# e=D_d_E[0]/(1-D_d_E[5]*D_d_E[3])

# K= T*Area*(BT*D*B)
BT_D=np.dot(Bt,matr_D)
BT_D_B=np.dot(BT_D,B)
K=D_d_E[9]*Area*BT_D_B
print("\nMatriz Bt*D")
print(BT_D)
print("\nMatriz Bt*D*B")
print(BT_D_B)
print("\nMatriz K")
print(K)

Lista_col=[]
Lista_Fil=[]

for i in range(8):
    Lista_col.append(list(K[:,i]))
    Lista_Fil.append(list(K[i]))

#MATRIZ DE ELEMENTOS---------------------------------------------------------------
'''---MATRIZ DE ELEMENTOS---'''

M_E_F=[] #Matriz de elementos finitos 
fila=[]
for i in range(1,Hx+1):        
    fila.append(i)
M_E_F.append(fila)

for j in range(1,Vy):
    fila=[]
    u=M_E_F[-1]    
    ult=u[-1]
    fin=ult+Hx+1
    for i in range(ult+1,fin):
        fila.append(i)
    M_E_F.append(fila)
M_E_F=np.array(M_E_F)
print('\nMATRIZ DE ELEMENTOS')
print(M_E_F) ##SE MUESTRA LA MATRIZ FORMADA

#MATRIZ DE NODOS-----------------------------------------------------------------
'''---MATRIZ DE NODOS---'''

M_N=[] #MATRIZ DE NODOS
lista=[]
for i in range(1,Hx+2):
    lista.append(i)
M_N.append(lista)
for j in range(1,Vy+1):
    lista=[]
    u=M_N[-1]    
    ult=u[-1]
    fin=ult+Hx+1
    for i in range(ult+1,fin+1):
        lista.append(i)
    M_N.append(lista)
M_N=np.array(M_N)
print('\nMATRIZ DE NODOS')
print(M_N)  ##SE MUESTRA LA MATRIZ FORMADA

print("\nCALCULANDO LA TABLA DE CONECTIVIDAD")
for i in tqdm(range(30001)):
    print("", end='\r')


#Tabla de conectividad----------------------------------------------------------
'''---TABLA DE CONECTIVIDAD---'''

C_G={} #CORDENADAS GLOBALES
## DICCIONARIO,CLAVES: NUMEROS DEL ELEMENTO, VALOR: COORDENADAS GLOBALES
for j in range(Vy):
          for i in range(Hx):
            '''print('ELEMENTO FINITO: {}'.format(M_E_F[j][i]))
            print('NODOS: {}, {}, {}, {}'.format(M_N[j+1][i],M_N[j][i],M_N[j][i+1],M_N[j+1][i+1]))'''
            C_G[M_E_F[j][i]]=[M_N[j+1][i],M_N[j][i],M_N[j][i+1],M_N[j+1][i+1]]
print('\n')            

C_L=[] #COORDENADAS LOCALES
##LISTA,POSICION: ELEMENTO FINITO, ELEMENTO: COORDENADAS LOCAL
for c in range(1,len(C_G)+1):
    lista=[]
    for v in range(4):
        xi=2*C_G[c][v]
        yi=2*C_G[c][v]-1
        lista.append(xi)
        lista.append(yi)
    C_L.append(lista)   


##SE IMPRIMEN LOS ELEMENTOS CON SUS RESPECTIVAS COORDENADAS GLOBALES Y LOCALES
contador=0
for c in C_G.keys():     
        print('\nElemento {} \n Coordenadas Globales {} \n Coordenadas Locales {}'.format(c,C_G[c],C_L[contador]))
        contador=contador+1

print("\nCALCULANDO MATRICES DE ELEMENTOS")
for i in tqdm(range(30001)):
    print("", end='\r')

# ENSAMBLE MATRIZ ELEMENTAL------------------------------------------------------

#Matrices desordenadas planteadas segun la tabla de conectividad 

print("\n------------------------Matrices Desordenadas--------------")

for i in range(len(C_L)):
    Matriz_Desordenada = pd.DataFrame(list(zip(Lista_col[0],Lista_col[1],Lista_col[2],Lista_col[3],Lista_col[4],Lista_col[5],Lista_col[6],Lista_col[7])), C_L[i], C_L[i])       
    print("---------------------------------------------------- ")
    print("Elemento {} ".format(i+1))
    print(Matriz_Desordenada)
    

print("\nORDENANDO LAS MATRICES DE ELEMENTOS")
for i in tqdm(range(30001)):
    print("", end='\r')

print("\n------------------------Matrices Ordenadas-----------------")
#Matrices ordenadas planteadas segun la tabla de conectividad 

Matriz_Ord_List=[]

for i in range(len(C_L)):
    Matriz_Desordenada = pd.DataFrame(list(zip(Lista_col[0],Lista_col[1],Lista_col[2],Lista_col[3],Lista_col[4],Lista_col[5],Lista_col[6],Lista_col[7])), C_L[i], C_L[i])       
    print("---------------------------------------------------- ")
    Matriz_Ordenada= Matriz_Desordenada.sort_index()
    Matriz_Ordenada= Matriz_Ordenada.reindex(columns=sorted(Matriz_Ordenada.columns))
    print("Elemento {} ".format(i+1))
    Matriz_Ord_List.append(Matriz_Ordenada)
    print(Matriz_Ordenada)
    
print("\nENSAMBLANDO LA MATRIZ ELEMENTAL ")
for i in tqdm(range(10001)):
    print("", end='\r')

# ENSAMBLAJE
T_C_L=[]
for i in range(1,(M_N.size*2)+1):
    T_C_L.append(i)
Matriz_E=pd.DataFrame(list(zip()),T_C_L,T_C_L)
Matriz_E=Matriz_E.fillna(0)
for e in Matriz_Ord_List:
    C_F.f_e_A(e,Matriz_E)

print("\n------------------------Matriz Elemental-----------------".center(60))
print(Matriz_E)

T_de_M=datetime.datetime.now()
T_de_Mstr=str(T_de_M.day)+"-"+str(T_de_M.month)+"-"+str(T_de_M.year)+" "+str(T_de_M.hour)+";"+str(T_de_M.minute)+";"+str(T_de_M.second)+".xlsx"
H_Excel=pd.ExcelWriter(T_de_Mstr)
Matriz_E.to_excel(H_Excel,sheet_name="Matriz Enlazada")

#---------------------------

Carga=C_F.validacion_float("\nCARGA (N): ")
S_C=pd.DataFrame(list(zip()),T_C_L,[1])
S_C=S_C.fillna(0)
M_N=list(M_N)
C_L=len(M_N[0])
if C_L==2:
    C=Carga/(C_L)
else: 
    C=Carga/(2*C_L-2)
C_L1=list(2*M_N[0]-1)
Lista=list()
for i in range(len(C_L1)):
    if i==0 or i==len(C_L1)-1: 
        Lista.append(-C)
    else:
        Lista.append(-2*C)
C_SC1=pd.DataFrame(list(zip(Lista)),C_L1,[1])
C_L2=list(2*M_N[-1]-1)
Lista=list()
for i in range(len(C_L2)):
    if i==0 or i==len(C_L2)-1:
        Lista.append(C)
    else:
        Lista.append(2*C)
C_SC2=pd.DataFrame(list(zip(Lista)),C_L2,[1])
C_SCarga=pd.concat([C_SC1,C_SC2])

S_C=C_SCarga+S_C
S_C=S_C.fillna(0) #Sistema de carga
print('\n------------------------Matriz de Sistema de Cargas------------------------')
print(S_C)
S_C.to_excel(H_Excel,sheet_name="Sistema de Carga")

Matriz_E=np.array(Matriz_E)
Inv=np.linalg.inv(Matriz_E) #Cuando tenemos 1 elemento en x y 1 elemento en y 
#el codigo tira un error en esta linea. VER PORQUE!
print('\n------------------------Matriz Inversa de Matriz de Ensamble------------------------\n')
print(Inv)

Desplazamientos=np.dot(Inv,S_C)
Desp=pd.DataFrame(list(zip(Desplazamientos)),T_C_L)
print('\n------------------------Matriz de Desplazamientos------------------------')
print(Desp) #Matriz de desplazamiento
Desp.to_excel(H_Excel,sheet_name="M_desplazamiento") 
Desp.to_csv('Desplazamientos.csv')

H_Excel.save()

print("\n\n\n\nDATOS GUARDADOS CORRECTAMENTE. ADJUNTADO EN LA UBICACION DEL ARCHIVO DEL ALGORITMO")
print('DATOS DE DESPLAZAMIENTOS ADJUNTADO EN LA UBICACION DEL ARCHIVO DEL ALGORITMO\n\n\n\n')
