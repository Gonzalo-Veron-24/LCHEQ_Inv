import numpy as np
import pandas as pd
from sympy import Symbol
import openpyxl
from sympy.core.facts import deduce_alpha_implications
import C_F as cf


def main():
    pd.options.mode.chained_assignment = None  # default='warn'
    print('¡Bienvenido! Por favor siga las instrucciones'.center(100),"\n","Universidad Nacional de Misiones (UNaM)".center(100),"\n","OBERÁ - MISIONES - ARGENTINA".center(100),"\n\n")
    CL=[-1,-1,1,-1,1,1,-1,1] #COORDENADAS LOCALES (SENTIDO ANTIHORARIO)


                                    #INGRESO DE DATOS DEL ELEMENTO FINITO
    while True:
        print("\n","INGRESE LAS DIMENSIONS DEL OBJETO".center(100))
        Ancho=cf.validacion_float("* Ancho(mm): ")                                   #Ancho= 180       | #Modulo Elastico 1 Datos_Ensayo[0]
        Alto=cf.validacion_float("* Alto(mm): ")                                     #Alto= 360        | #Modulo Elastico 2 ...[1]
        Area=Alto*Ancho                                                              #Hx = 18         | #Modulo Elastico 3 ...[2]
        print("\n","* Área(mm^2): {}".format(Area))                                  #Vy = 36         | #Deformación Correlativa (idc12) ...[3]
        AreaF=4*Area                                                                 #E panel= 9860   | #Deformación Correlativa (idc13) ...[4]
        Hx=int(cf.validacion_float("\nIngrese la cantidad de elementos en X: "))     #E celdas= 894   | #Deformación Correlativa (idc13) ...[5]
        Vy=int(cf.validacion_float("\nIngrese la cantidad de elementos en Y: "))     #idc12=0.19      | #Valor promedio de ancho L1 ...[6]
                                    #INGRESO DE DATOS DE ENSAYO                      #L1= ancho= 173.3| #Factor de ajuste incremental ...[7]
        Datos_Ensayo=[]                                                              #n= Ft/Et        | #Modulo traccion ...[8]
        cf.ingreso_datos_ensayo(Datos_Ensayo)                                        #λ=0.5           | #Resistencia traccion ...[9]
                                                                                    #ft: 2.23 MPa    | #L1 ...[10]
                                                                                    #Et: 606 MPa     | #Espesor Equivalente ...[11]
                                                                                    #λ: 0.5          | #G12 [12], G13 [13], G23 [14]
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
        L1: {}
        Espesor equivalente (T): {}
        
        """.format(Ancho, Alto, Area, AreaF, Hx, Vy, *Datos_Ensayo))
        op=input("\n¿Los datos ingresados son correctos?\n1 - Continuar\n2 - Reingresar\n... ")
        if op=="1": break
        elif op=="2": print("\n","-------------------- DATOS ELIMINADOS --------------------".center(100))
        else: print("\n¡OPCION NO VALIDA!\n")

    #---------------------------------DATOS UTILIZADOS-------------------------------------
    #Carga1= +33.71141565 | #DefE1= 0.0008542475559706115 | #DespProm1= 0.30752912014942013
    #Carga2= +34.08419166 | #DefE2= 0.0008636937031978038 | #DespProm2= 0.31092973315120936
    #Carga3= +28.49287563 | #DefE3= 0.0007220097079934437 | #DespProm3= 0.2599234948776397
    #Carga4= +34.57030922 | #DefE4= 0.0008760119262548176 | #DespProm4= 0.31536429345173433
    #Carga5= +34.65797708 | #DefE5= 0.0008782334305642091 | #DespProm5= 0.3161640350031153
    #Carga6= +34.73208359 | #DefE6= 0.0008801112901505955 | #DespProm6= 0.3168400644542144
    #Carga7= +22.63870073 | #DefE7= 0.0005736648668135243 | #DespProm7= 0.20651935205286875

    Xi, ita = Symbol("Xi"), Symbol("ita")
    Nodo_list=[(1/4)*(1-Xi)*(1-ita),(1/4)*(1+Xi)*(1-ita),(1/4)*(1+Xi)*(1+ita),(1/4)*(1-Xi)*(1+ita)] #Func. Forma

    cf.barra_carga()
    Fecha=cf.fecha()
    H_Excel=pd.ExcelWriter(Fecha) #creo el archivo excel
    H1 = pd.DataFrame(Nodo_list, index = ["1","2","3","4"])
    H1.to_excel(H_Excel, sheet_name='Funciones de Formas', index=False) 
    H_Excel.close() #a partir de esta sentencia trabajo con la funcion creada

                                # DERIVADAS PARCIALES (Preguntar porque no se utiliza)
    # DNL=[] #Lista de derivadas de los nodos
    # for i in Nodo_list:
    #     dNdXi=i.diff(Xi)
    #     dNdita=i.diff(ita)
    #     DNL.append(dNdXi)
    #     DNL.append(dNdita)

    M_E_F=cf.M_E(Hx,Vy)                                     # | MATRIZ DE ELEMENTOS FINITOS
    M_N=cf.M_N(Hx,Vy)                                       # | MATRIZ DE NODOS
    T_C_L=[x for x in range(1,(M_N.size*2)+1)]                            
    C_G_L=cf.T_C(Hx,Vy,M_E_F,M_N)                           # | TABLA DE CONECTIVIDAD
    D_Generales=cf.D_G(Hx,Vy,Ancho,Alto)                    # | DISTANCIAS GENERALES
    C_L = cf.coord_loc(C_G_L,D_Generales)                   # | Coordenadas Locales
    T_i=cf.T_I(Nodo_list,D_Generales,Xi,ita)                # | TRANSFORMACIÓN ISOPARAMÉTRICA  
    j_i_d = cf.J_I_D(T_i)                                   # | JACOBIANOS, INVERSAS Y DETERMINANTES
    A = cf.M_A(j_i_d)                                       # | MATRICES A
    G = cf.M_G(Xi, ita)                                     # | MATRIZ G
    Bt = {}                                                 # | MATRICE B Y Bt
    B = cf.M_B(A,G,Bt)
    B_numerico = cf.B_valores(CL,B,Xi,ita)                  # | B con sus respectivos valores
    D = cf.M_D(Datos_Ensayo)                                # | MATRIZ D    
    K = cf.M_K(B,Bt,D,Xi,ita,j_i_d,Datos_Ensayo[11],C_G_L)  # | MATRICES K
    M_E = cf.f_e_B(M_N,K,T_C_L,H_Excel,Fecha)                             # | ENSAMBLE
    M_E_n = np.array(M_E)
    M_E_ni = np.linalg.inv(M_E_n)
    Cant_C = cf.validar_dato(1,10,"CANTIDAD DE ENSAYOS")    # | Cantidad de ensayos


    dict_sist_carga = {}
    dict_desplazamientos = {}
    dic_tensiones = {}
    dic_deformaciones = {}
    for i in range(Cant_C):
        #Ingreso de la carga
        Carga = cf.validacion_float("\nCarga (N): ")
        #Calculo del sistema de cargas (Sin ordenar)
        sistema_carga = cf.S_C(Carga,M_N,T_C_L)
        #Calculo de los desplazamientos (Sin ordenar)
        Desplazamientos = pd.DataFrame(np.dot(M_E_ni,sistema_carga),index=T_C_L) #Revisar porque las nuevas versiones nos hacen variar tanto el resultado

        #Funcion que ordena los desplazamientos, el sistema de cargas
        #los guarda dentro de sus respectivos diccionarios
        #y dentro del excel
        cf.funct_ord_cl(Desplazamientos,sistema_carga,C_L,dict_desplazamientos,dict_sist_carga,Carga,H_Excel,Fecha)
        print(dict_desplazamientos[f"{Carga}"])

        #Carga por elemento
        corrimiento_x_elem = cf.sep_por_elem(dict_desplazamientos[f"{Carga}"],Desplazamientos,C_L)
        
        #Calculamos las tensiones y deformaciones y las guardamos en un diccionario
        cf.tens_deformaciones(Hx,Vy,D,B_numerico,corrimiento_x_elem,dic_tensiones,dic_deformaciones,C_G_L)

        #Calculamos la deformacion especifica
        D_especifica = cf.D_E(Desplazamientos,Alto,Vy)
        print("\nLa Deformacion especifica es igual a: {}\n".format(D_especifica))
        cf.tensiones_deformaciones_excel(dic_tensiones,dic_deformaciones,C_G_L,Carga,H_Excel,Fecha)

main()