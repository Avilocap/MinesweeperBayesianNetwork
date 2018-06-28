Índice:

1. Introducción
2. Composición del código
	2.1. Generación
	2.2. Resolución
3. Pruebas

1. Introducción:
El objevido de este fichero es exponer la composición del código fuente así como las instrucciones necesarias para ejecutar las pruebas realiadas en la elaboración del documento adjunto.

2. Composición del código:
El código se compone de dos partes fundamentales.

	2.1.Generación:
	Esta parte se encarga de la genración del tablero del buscaminas y la red bayesiana asociada;
	Los archivos que generan el tablero son: 
		-msboard.py
		-msgame.py
	El archivo que genera la red bayesiana es:
		-BayesianNetworkGenerator.py

	2.2. Resolución:
	La segunda parte importante del programa es la que se encarga de ejecutar la red bayesiana sobre el juego del buscaminas. Podemos encontrar dos elementos:
		- autosolver.py: Se trata de una definición que dado un tamaño de tablero y un número de minas, realiza la resolución del tablero de inicio a fin haciendo click en las casillas automaticamente
		- nextStep.py: Este elemento realiza la misma acción que el anterior con la diferencia de que en cada iteración se consulta al jugador si desea hacer click en las casilla predicha.
		- repeater.py: Este archivo se trata de un fichero de pruebas en el que dado un array con combinaciones de (tamaño de tablero, número de minas) llama al fichero autosolver.py tantas veces como combinaciones haya, con la peculiaridad de que no pasará al siguienten elemento hasta que haya completado con exito el tablero que se encuentra iterando. Esta funcionalidad nos brinda la posibilidad de realizar todas las pruebas juntas y asegurarnos de que no va a parar hasta haberlas realizado satisfactoriamente.

3.Pruebas
Las pruebas realizadas en el apartado Pruebas de Rendimiento han sido realizando ejecutando con Python 3 el fichero repeater.py ya que dicho fichero contiene todas las pruebas requeridas por los requisitos, estas pruebas han sido realizadas completamente un total de 3 veces.

Sin embargo, si se desea realizar una prueba en concreto, bastaría con editar el tamaño del tablero y el número de minas de la línea 13 del fichero individualAutosolver.py y ejecutarlo con python3. El terminal mostrará entonces la ejecución del programa.

! El tablero debe ser una matriz cuadrada de tamaño mxm ! 

 * SON NECESARIOS LOS SIGUENTES PAQUETES: 
		- pgmpy
		- numpy
		- networkx
		- pandas