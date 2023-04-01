import numpy as np
import pandas as pd
from sympy import Symbol
import openpyxl
import datetime
from sympy.core.facts import deduce_alpha_implications
from tqdm.auto import tqdm
import C_F as cf
import os
import copy

pd.options.mode.chained_assignment = None  # default='warn'
print('¡Bienvenido! Por favor siga las instrucciones'.center(100),"\n","Universidad Nacional de Misiones (UNaM)".center(100),"\n","OBERÁ - MISIONES - ARGENTINA".center(100),"\n\n")
CL=[-1,-1,1,-1,1,1,-1,1] #COORDENADAS LOCALES (SENTIDO ANTIHORARIO)


                                #INGRESO DE DATOS DEL ELEMENTO FINITO
while True:
    print("\n","INGRESE LAS DIMENSIONS DEL OBJETO".center(100))
    Ancho=cf.validacion_float("* Ancho(mm): ")
    Alto=cf.validacion_float("* Alto(mm): ")
    Area=Alto*Ancho
    print("\n","* Área(mm^2): {}".format(Area))
    AreaF=4*Area    ####################### CONSULTAR #######################
    
    Hx=int(cf.validacion_float("\nIngrese la cantidad de elementos en X: "))
    Vy=int(cf.validacion_float("\nIngrese la cantidad de elementos en Y: "))
                                #INGRESO DE DATOS DE ENSAYO
    
    Datos_Ensayo=[]
    cf.ingreso_datos_ensayo(Datos_Ensayo)
    #Modulo Elastico 1 Datos_Ensayo[0]
    #Modulo Elastico 2 Datos_Ensayo[1]
    #Modulo Elastico 3 Datos_Ensayo[2]
    #Deformación Correlativa (idc12) Datos_Ensayo[3]
    #Deformación Correlativa (idc13) Datos_Ensayo[4]
    #Deformación Correlativa (idc13) Datos_Ensayo[5]
    #Valor promedio de ancho L1 D_d_E[6]
    #Factor de ajuste incremental D_d_E[7]
    #Modulo traccion D_d_E[8]
    #Resistencia traccion D_d_E[9]
    print("""
    --------------- DATOS INGRESADOS: ---------------
    Ancho(mm): {}
    Alto(mm): {}
    Área(mm^2): {}
    Área del Elemento Finito: {}
    Cantidad de elementos en X: {}
    Cantidad de elementos en Y: {}
    Módulo Elástico (E1): {}
    Módulo Elástico (E2): {}
    Módulo Elástico (E3): {}
    Deformación Correlativa (idc12): {}
    Deformación Correlativa (idc13): {}
    Deformación Correlativa (idc32): {}
    Valor promedio de ancho (L1): {}
    Factor de Ajuste incremental (λ): {}
    Modulo Tracción (Et): {}
    Resistencia Tracción (Ft): {}
    L1 = {}
    
    """.format(Ancho, Alto, Area, AreaF, Hx, Vy, *Datos_Ensayo))
    op=input("\n¿Los datos ingresados son correctos?\n1 - Continuar\n2 - Reingresar\n... ")
    if op=="1": break
    elif op=="2": print("\n","-------------------- DATOS ELIMINADOS --------------------".center(100))
    else: print("\n¡OPCION NO VALIDA!\n")


#Ancho= 36
#Alto= 36
# 10x10
#E panel= 9860
#E celdas= 894
#idc12=0.19

#L1= ancho= 173.3                              
#n= Ft/Et
#λ=0.5

# T1= n*(L1**λ)
# T2= λ(Ln*n)
# T3= (λ/n)*L1
# T4= (n/λ)*L1


#ft: 2.23 MPa
#Et: 606 MPa
#λ: 0.5

#Carga1= +33.71141565 
#Carga2= +34.08419166 
#Carga3= +28.49287563
#Carga4= +34.57030922
#Carga5= +34.65797708
#Carga6= +34.73208359
#Carga7= +22.63870073

#DefE1= 0.0008542475559706115
#DefE2= 0.0008636937031978038
#DefE3= 0.0007220097079934437
#DefE4= 0.0008760119262548176
#DefE5= 0.0008782334305642091
#DefE6= 0.0008801112901505955
#DefE7= 0.0005736648668135243

#DespProm1= 0.30752912014942013
#DespProm2= 0.31092973315120936
#DespProm3= 0.2599234948776397
#DespProm4= 0.31536429345173433
#DespProm5= 0.3161640350031153
#DespProm6= 0.3168400644542144
#DespProm7= 0.20651935205286875

L1=1
Datos_Ensayo.append(L1)

while True: # SELECCIÓN DEL TIPO DE ESTRUCTURA
    print("\n¿Con qué tipo de estructura regional desea trabajar?".center(100),"\n1 - Ladrillo macizo\n2 - Ladrillo hueco\n\n")
    op=input(">>> ")
    if op=="1":
        tipo=False
        break
    elif op=="2":
        tipo=True
        break
    print("OPCIÓN INCORRECTA".center(100),"\n","POR FAVOR REINGRESE".center(100))
if tipo:                        #LADRILLO HUECO
    pass
else:                           #LADRILLO MACIZO
    #T=(D_d_E[7]/(D_d_E[9]/D_d_E[8]))*D_d_E[6]
    T=1
    Datos_Ensayo.append(T)
    
    G12= float(Datos_Ensayo[0]/(2*(1+Datos_Ensayo[3])))
    Datos_Ensayo.append(G12)
    G13= float(Datos_Ensayo[0]/(2*(1+Datos_Ensayo[4])))
    Datos_Ensayo.append(G13)
    G23= float(Datos_Ensayo[1]/2/(1+Datos_Ensayo[5]))
    Datos_Ensayo.append(G23)
    
    print("\n\n","EL ALGORITMO COMENZARÁ A HACER LOS CÁLCULOS CORRESPONDIENTES","\n\n")
    for i in tqdm(range(4000)):
        print("", end=("\r"))
    print(Datos_Ensayo)
                                # FUNCIONES DE FORMA
    Xi = Symbol("Xi")
    ita = Symbol("ita")
    N1,N2,N3,N4=(1/4)*(1-Xi)*(1-ita),(1/4)*(1+Xi)*(1-ita),(1/4)*(1+Xi)*(1+ita),(1/4)*(1-Xi)*(1+ita)
    Nodo_list=[N1,N2,N3,N4]
    
    T_de_M=datetime.datetime.now()
    T_de_Mstr=str(T_de_M.day)+"-"+str(T_de_M.month)+"-"+str(T_de_M.year)+" "+str(T_de_M.hour)+";"+str(T_de_M.minute)+";"+str(T_de_M.second)

    H_Excel=pd.ExcelWriter(T_de_Mstr+".xlsx")
    H1 = pd.DataFrame(Nodo_list, index = ["1","2","3","4"])
    H1.to_excel(H_Excel, sheet_name='Funciones de Formas', index=False)                     
                                # DERIVADAS PARCIALES
    DNL=[] #Lista de derivadas de los nodos
    for i in Nodo_list:
        dNdXi=i.diff(Xi)
        dNdita=i.diff(ita)
        DNL.append(dNdXi)
        DNL.append(dNdita)
                                # MATRIZ DE ELEMENTOS FINITOS
    M_E_F=cf.M_E(Hx,Vy)

                                # MATRIZ DE NODOS
    M_N=cf.M_N(Hx,Vy)


    T_C_L=[x for x in range(1,(M_N.size*2)+1)]

                                # TABLA DE CONECTIVIDAD
    C_G_L=cf.T_C(Hx,Vy,M_E_F,M_N)
                                # DISTANCIAS GENERALES
    D_Generales=cf.D_G(Hx,Vy,Ancho,Alto)
    
    C_L = []
    for i in C_G_L.keys():
        print("\nElemento N°{}: \nCoordenadas Globales: {} \nCoordenadas Locales: {} \nDistancias en X: {} \nDistancias en Y: {}".format(i,C_G_L[i][0],C_G_L[i][1],D_Generales[i][0],D_Generales[i][1]))
        for e in C_G_L[i][1]:
            C_L.append(e)
                                # TRANSFORMACIÓN ISOPARAMÉTRICA

    T_i=cf.T_I(Nodo_list,D_Generales,Xi,ita)
                                #JACOBIANOS, INVERSAS Y DETERMINANTES
    j_i_d = cf.J_I_D(T_i)
                                #MATRICES A
    A = cf.M_A(j_i_d)
                                #MATRIZ G
    G = cf.M_G(Xi, ita)
                                #MATRICE B Y Bt
    Bt = {}
    B = cf.M_B(A,G,Bt)

    B_numerico = copy.deepcopy(B) ##B con sus respectivos valores
    cf.B_valores(CL,B_numerico,Xi,ita)
    
                                #MATRIZ D
    D = cf.M_D(Datos_Ensayo)
                                #MATRICES K
    K = cf.M_K(B,Bt,D,Xi,ita,j_i_d,T,C_G_L)
    
                                #ENSAMBLE
    M_E = cf.f_e_B(M_N,K,T_C_L)

    while True:
        try:
            Cant_C = int(input("\nIngrese la cantidad de ensayos a analizar: "))
            break
        except ValueError:
            print("\n¡ERROR! Reingrese!")

    E = 9860
    Des = {}   
    Des_esp = {}
    ten_m1 = {}
    tensiones_m2 = {}
    cargas_p_ele = {}
    for i in range(Cant_C):
        
        Carga = cf.validacion_float("\nCarga (N): ")

        s_c = cf.S_C(Carga,M_N,T_C_L)
        s_c.to_excel(H_Excel,sheet_name="Sist. Q={}".format(Carga))
        print("\nSistema de Cargas: \n{}".format(s_c))

        #Desplazamientos
        M_E_n = np.array(M_E)
        M_E_ni = np.linalg.inv(M_E_n)

        Desplazamientos = pd.DataFrame(np.dot(M_E_ni,s_c),index=T_C_L)

        D_e_o = pd.DataFrame([0.0 for i in range(len(C_L))],index=C_L)
        Sist_c_o = pd.DataFrame([0.0 for i in range(len(C_L))],index=C_L)
        
        for j in Desplazamientos.index:
            for e in D_e_o.index:
                if j == e:
                    D_e_o[0][e] = Desplazamientos[0][e]
                    Sist_c_o[0][e] = s_c[1][e] 
        
        print("\nSistema de Cargas ordenados por c_l: \n{}".format(Sist_c_o))
        Sist_c_o.to_excel(H_Excel,sheet_name="Sist ord. Q={}".format(Carga))

        print("\nDesplazamientos:\n{}".format(D_e_o))
        D_e_o.to_excel(H_Excel,sheet_name="Desplaz. Q={}".format(Carga))


        ##Deformacion especifica
        paso = D_e_o.copy() #Creo una copia del dataframe de desplzamientos
        Des[i+1] = paso

        for h in range(1,(Desplazamientos.index[-1])+1):
            if h%2==0: 
                (D_e_o[0][h])/=Alto
            else:
                (D_e_o[0][h])/=Ancho

        paso2 = D_e_o.copy()
        Des_esp[i+1] = paso2
        Des_esp[i+1].to_excel(H_Excel,sheet_name="Desplaz_esp. Q={}".format(Carga))

        ##METODO 1
        ten_m1[i+1] = (D_e_o*E)
        ten_m1[i+1].to_excel(H_Excel,sheet_name="tensiones. Q={}".format(Carga))
        
        c_p_e = cf.sep_por_elem(Sist_c_o,s_c,C_L)
        cargas_p_ele[i+1] = c_p_e

        ##TENSIONES METODO 2 D*B*q
        tensiones_m2[i+1] = cf.tens_m2(Hx,Vy,D,B_numerico,c_p_e) 
        '''
        tensiones_m2 es un diccionario que como clave tiene el numero de todos los elementos
        ej: un valor es 1, el otro 2 y asi hasta 100 que en este caso es nuestro ultimo elemento.
        Cada uno de esas claves tiene otro diccionario como valor. Dicho diccionario contiene 4 pares
        clave-valor, las claves son 1,2,3,4 (nodos) y como valor contienen una lista con las 3 tensiones
        '''

        #Deformacion especifica
        D_especifica = cf.D_E(Desplazamientos, Alto, Vy)
        print("\nLa Deformacion especifica es igual a: {}\n".format(D_especifica))
    H_Excel.save()
    print("Tensiones")
    print(tensiones_m2[1][1][1][1])


