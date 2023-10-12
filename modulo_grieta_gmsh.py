import gmsh 

def malla(elem_x, elem_y, tam_x, tam_y):
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)

    gmsh.model.add("modelo_1")

    #Tamaño de malla en todos los puntos
    tm = 1

    #Agregamos los 4 puntos limites
    gmsh.model.geo.addPoint(0,0,0,tm,1)
    gmsh.model.geo.addPoint(elem_x*tam_x,0,0,tm,2)
    gmsh.model.geo.addPoint(elem_x*tam_x,elem_y*tam_y,0,tm,3)
    gmsh.model.geo.addPoint(0,elem_y*tam_y,0,tm,4)

    #Creamos lineas
    gmsh.model.geo.addLine(1,2,1)
    gmsh.model.geo.addLine(2,3,2)
    gmsh.model.geo.addLine(3,4,3)
    gmsh.model.geo.addLine(4,1,4)

    # Para definir superficies, primero se deben definir 'Curve Loops' que las
    # limiten.
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)

    # Dado que queremos una malla estructurada, definimos el número de elementos
    # que queremos en ciertas líneas:
    # Sintaxis: gmsh.model.geo.mesh.setTransfiniteCurve(tag, # nodos)
    for tag in range(1,5):
        if tag%2 != 0: gmsh.model.geo.mesh.setTransfiniteCurve(tag, elem_x+1)    
        else: gmsh.model.geo.mesh.setTransfiniteCurve(tag, elem_y+1)
    
    # Ahora sí se puede definir la superficie, así:
    #Sintaxis: gmsh.model.geo.addPlaneSurface([Lista de Curve Loops], tag), donde:
    #          En la lista de Curve Loops el primer elemento es el loop que define
    #          el contorno de la superficie, los demás son agujeros dentro de ella.

    s1 = gmsh.model.geo.addPlaneSurface([1], 1)

    s = gmsh.model.addPhysicalGroup(2, [1]) # En este caso no se especifica tag
    gmsh.model.setPhysicalName(2, s, "Mi superficie")  # Se puede definir un nombre

    gmsh.model.geo.mesh.setTransfiniteSurface(s1)
    gmsh.model.geo.mesh.setRecombine(2,s1)
    gmsh.model.geo.synchronize()
    gmsh.option.setNumber('Mesh.SurfaceFaces', 1)
    gmsh.option.setNumber('Mesh.Points', 1)
    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()
    gmsh.finalize()

if __name__ == '__main__':
    elem_x = 10
    elem_y = 15
    tam_x = 36
    tam_y = 36
    malla(elem_x,elem_y,tam_x,tam_y)
