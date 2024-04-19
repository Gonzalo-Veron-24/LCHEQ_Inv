<h1 align="center"> Caracterización de sistemas alternativos de mamposterías regionales </h1>
<h1 align="center"> Facultad de Ingeniería UNAM </h1>
<p align="center">
  <img width="100%" height="350" src="https://github.com/Gonzalo-Veron-24/LCHEQ_Inv/assets/77847783/a3df8c9a-d000-47cb-b9d1-af37f16d15d3">
</p>

## Teoría
### Introducción
Esta herramienta facilita la generación de resultados representativos del comportamiento experimental de probetas sometidas a compresión. El proceso modela las tensiones, los desplazamientos y las grietas generadas durante la rotura de las mismas (actualmente en desarrollo), empleando el método de elementos finitos. Si bien este método no proporciona resultados exactos, ofrece aproximaciones lo suficientemente precisas como para estimar los valores reales.

### Marco teórico
El Método de Elementos Finitos es una técnica general para la solución de problemas de contorno regidos por ecuaciones ordinarias y/o parciales. Esta metodología reemplaza el problema diferencial por otro algebraico equivalente. Una de las técnicas reconocidas para la resolución implica la discretización o subdivisión de una región, sobre la cual están definidas ecuaciones en forma geométrica, en elementos finitos. Las propiedades materiales y las relaciones gobernantes en estos elementos se expresan en función de los valores desconocidos en los nodos del elemento en cuestión.

### Desarrollo teórico
Como primer paso, se enumera los nodos de manera acorde y se lo lleva a un sistema de coordenadas locales ξ(zita) y η(eta). Para determinar el comportamiento de cada elemento, se debe determinar el comportamiento de los nodos mediante las funciones de forma (N).
<p align="center">
  <img width="400" height="150" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.24.01_vd6av7.jpg">
</p>

Luego se realiza la interpolación de los desplazamientos nodales para la obtención del campo de desplazamiento de cada elemento, la cual se expresará en las coordenadas globales X e Y en términos de las funciones de forma.
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.24.40_acw9qs.jpg">
</p>

A continuación se realiza la resolución de las derivadas parciales de cada campo de desplazamiento para obtener una relación entre ambas coordenadas, la herramienta matemática que nos permitirá realizar este paso es una matriz Jacobiana (1).
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.25.39_fmccj9.jpg">
  <img width="150" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533369/WhatsApp_Image_2024-04-19_at_10.25.51_xq9ukn.jpg">
</p>

Matriz Jacobiana desarrollada:
<p align="center">
  <img width="800" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533369/WhatsApp_Image_2024-04-19_at_10.26.06_fabhpj.jpg">
</p>

En este apartado, invertimos la ecuación (1) para poder obtener la relación:
<p align="center">
  <img width="150" height="50" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.26.20_xsuqk7.jpg">
  <img width="500" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.26.50_znop3p.jpg">
</p>

Relacionando las deformaciones unitarias de las vigas con las tensiones existentes, a partir de una serie de ecuaciones, resultará la matriz de rigidéz elemental (K):
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.27.04_bajvme.jpg">
</p>

D es la matriz de propiedades del material en estado de tensión plana (E: modulo de elasticidad; v: Coeficiente de Poisson):
<p align="center">
  <img width="200" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.27.09_jnlna0.jpg">
</p>

Para deducir la matriz isoparamétrica B, se utilizaron las siguientes expresiones: 
<p align="center">
  <img width="500" height="150" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.27.24_fjqjay.jpg">
</p>
<p align="center">
  <img width="800" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.27.32_xqig9k.jpg">
</p>

Donde:
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533370/WhatsApp_Image_2024-04-19_at_10.27.38_buoici.jpg">
</p>

Teniendo en cuenta las deformaciones:
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533369/WhatsApp_Image_2024-04-19_at_10.27.41_h182ln.jpg">
</p>

Y las tensiones:
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533369/WhatsApp_Image_2024-04-19_at_10.27.43_opguo2.jpg">
</p>

Mediante el vector de desplazamiento globales (Q), se hallan los desplazamientos nodales (q) (K: Matriz de ensamble; F: vector de fuerzas):
<p align="center">
  <img width="300" height="100" src="https://res.cloudinary.com/dq9faptjc/image/upload/v1713533369/WhatsApp_Image_2024-04-19_at_10.27.47_cvlbw8.jpg">
</p>

## Instalación
**El proyecto solo esta disponible para versiones de python 3.9.x** (Puede utilizar [pyenv](https://github.com/pyenv-win/pyenv-win))
### Entorno Virtual
Se recomienda crear un entorno virtual en su computadora, puede utilizar [virtualenv](https://rkadezone.wordpress.com/2020/09/14/pyenv-win-virtualenv-windows/).
Luego de crearlo, se debera instalar las dependencias necesarias especificadas en el archivo de texto _requirements.txt_. Puede utilizar el siguiente comando:

```
pip install -r .\requirements.txt
```

## Funcionamiento del código:
El procedimiento teórico previamente discutido se implementa en el código de manera rápida y eficiente, permitiendo la variación de diversos parámetros de entrada para modelar distintos escenarios. Como resultado, se obtienen las tensiones y los desplazamientos nodales.
Al iniciar una corrida, se solicitará que se ingresen los siguientes datos:
- Ancho del elemento (mm).
- Alto del elemento(mm).
- Cantidad de elementos en X (cuanto queremos discretizar en x).
- Cantidad de elementos en Y (cuanto queremos discretizar en y).
- Módulo Elástico (E).
- Deformación Correlativa (idc12).
- Deformación Correlativa (idc13).
- Deformación Correlativa (idc32).
- Factor de Ajuste incremental (λ).
- Modulo Tracción (Et).
- Resistencia Tracción (Ft).
- Espesor equivalente (T).

Unos segundos después, se le solicitará que ingrese la cantidad de cargas que desea ensayar. Posteriormente, deberá ingresar el valor de dichas cargas en Newtons. Una vez finalizada la corrida, se habrá exportado un archivo Excel con los datos correspondientes de cada análisis.

## Desarrollo actual
Actualmente, se está desarrollando una representación gráfica de la mampostería analizada y la grieta correspondiente generada en su estado de rotura. Para este desarrollo, se está utilizando una biblioteca específica diseñada para trabajar con el método de elementos finitos, denominada [GMSH](https://gmsh.info/doc/texinfo/gmsh.html)
