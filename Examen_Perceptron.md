# Evaluacion examen_perceptron_mlp_cnn_grupoA <br>
<br>

          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            EXAMEN TEÓRICO — PERCEPTRÓN, MLP Y CNN (GRUPO A)

                            Eduardo Alcaraz
          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1 Datos del alumno <br>
══════════════════

  ━━━━━━━━━━━ <br>
   Nombre  Correa Cervantes Diego Ignacio <br>
   Grupo   A <br>
   Fecha   3/11/2026 <br>
  ━━━━━━━━━━━ <br>
<br>

2 Pregunta 1 — Idea del perceptrón <br>
══════════════════════════════════ <br>

  1. Explica qué recibe un perceptrón, qué hace con los pesos y el bias,
     y qué produce. <br>
  2. ¿Qué quiere decir que dos clases sean *linealmente separables*? <br>
  3. Señala *una* limitación fuerte del perceptrón de una sola capa. <br>
<br>

2.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. Un perceptrón recibe varios datos numéricos de entrada, a los que les asigna una importancia (pesos) y les suma un ajuste inicial (bias). Luego, junta todo en una suma y, si esa suma pasa un umbral, da como resultado un valor (por ejemplo, 1 o 0, "sí" o "no"). <br>
    2. Significa que puedes dividir dos grupos de datos trazando una línea recta entre ellos en una gráfica. <br>
    3. No puede resolver problemas donde los datos no se puedan separar con una línea recta <br>
  └──── <br>


3 Pregunta 2 — Por qué aparece el MLP <br>
═════════════════════════════════════ <br>

  1. ¿En qué sentido un MLP es “más de una capa de neuronas”? <br>
  2. ¿Para qué sirve la capa oculta ? <br>
  3. Si quitas todas las activaciones no lineales, ¿qué tipo de
     comportamiento te queda y por qué importa? <br>
<br>

3.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. Se refiere a que ya no hay solo una neurona procesando datos, sino varias neuronas organizadas en niveles o "pisos" intermedios. <br>
    2. Funciona como un procesador intermedio que ayuda a descubrir combinaciones o patrones complejos que una sola neurona no puede ver por si sola. <br>
    3. Si le quitas las funciones no lineales, todas las capas acumuladas equivalen a una sola línea recta simple. Perdiendo la capacidad de aprender patrones complejos. <br>
  └──── <br>


4 Pregunta 3 — XOR como lección histórica <br>
═════════════════════════════════════════ <br>

  1. ¿Qué enseña el ejemplo XOR sobre el perceptrón simple? <br>
  2. ¿Qué cambia al pasar a una red con capas ocultas y no linealidad? <br>
  3. ¿Eso significa que el perceptrón nunca sirve en problemas reales?
     Argumenta. <br>
<br>

4.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. El perceptrón simple falla por completo cuando se le pide resolver un problema tan básico que no puede dividirse con una linea recta. <br>
    2. Al añadir capas ocultas y funciones no lineales, la red ya puede doblar o curvar sus decisiones, logrando resolver problemas no lineales como XOR. <br>
    3. Sirve en casos como problemas sencillos donde la decisión depende de un solo corte directo (como predecir algo con solo dos opciones muy marcadas), en esos casos es rápido, eficiente y fácil de usar. <br>
  └──── <br>


5 Pregunta 4 — Cómo “aprende” la red <br>
════════════════════════════════════ <br>

  1. Describe con palabras el ciclo: predicción → medir error → ajustar
     pesos. <br>
  2. ¿Qué controla el *learning rate* (tasa de aprendizaje) a nivel
     conceptual? <br>
  3. Diferencia *subajuste* y *sobreajuste* con un ejemplo escolar
     breve. <br>
<br>

5.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. En la predicción la red hace una suposición con lo que sabe hasta el momento. Al medir error compara la suposición con el resultado real para ver qué tanto se equivocó. Finalmente al ajustar pesos Modifica poco a poco sus conexiones internas para fallar menos en la siguiente oportunidad. <br>
    2. Es la velocidad a la que se corrigen los pesos; si esta es muy alta, da saltos desesperados y se equivoca; si es muy baja, tarda demaciado en aprender. <br>
    3. El subajuste se refiere a cuando un peso no logra llegar a una cantidad que permita una prediccion correcta, el sobreajuste por su parte a cuando rebasa la cantidad esperada (mas de 1 en AND o XOR).Como ejemplo podemos tomar un reloj que se ajusta manualmente, la hora exacta son las 9:00 am si al ajustar la rueda del reloj se para un poco antes de que las agujas queden en la posicion correcta se tendria un subajuste. Si por el contrario se para un poco despues de que las agujas lleguen entonces se tendra un sobreajuste. <br>
  └──── <br>


6 Pregunta 5 — Salidas: sigmoide y softmax <br>
══════════════════════════════════════════ <br>

  1. ¿Cuándo usarías sigmoide y cuándo softmax? <br>
  2. ¿Qué significa el vector que sale de un softmax en un problema de
     varias clases? <br>
  3. Pon un ejemplo del curso (juego, riesgo, imágenes, etc.) y di qué
     salida encajaría. <br>
<br>

6.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. Usaria la sigmoide para preguntas de "sí/no" o para clasificar algo en una sola categoría independiente. Por el contrario usaria softmax para elegir una única opción entre tres o más categorías posibles. <br>
    2. Significa una lista de porcentajes o probabilidades para cada categoría posible, donde la suma de todas da el 100% <br>
    3. Tomando el caso del CNN para identificar rostros, el dataset representa las categorias y a la hora de identificarlos softmax indica cual es el mas probable segun las caracteristicas de cada imagen. 
  └──── <br>


7 Pregunta 6 — Motivación de la CNN <br>
═══════════════════════════════════ <br>

  1. ¿Qué inconveniente conceptual tiene aplastar una imagen y meterla a
     un MLP denso? <br>
  2. ¿Qué aporta la idea de *filtro local* y *pesos compartidos*? <br>
  3. Menciona *dos* dominios (además de fotos cotidianas) donde una CNN
     tiene sentido. <br>
<br>

7.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. Se destruye la relación de espacio entre los píxeles (se pierde la noción de qué está arriba, abajo o al lado de qué) y se genera una cantidad absurda de parámetros. <br>
    2. Permiten examinar la imagen por parches pequeños usando el mismo "lente" repetidamente, reconociendo un objeto en cualquier parte donde aparezca sin multiplicar las conexiones. <br>
    3. Identificar imagenes medicas o espectrogramas <br>
  └──── <br>


8 Pregunta 7 — Piezas de una CNN <br>
════════════════════════════════ <br>

  Explica el *para qué* de: <br>
  1. Convolución <br>
  2. Pooling <br>
  3. Flatten + Dense al final <br>
  4. Dropout durante el entrenamiento <br>
<br>

8.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. Escanea la imagen para detectar características básicas como bordes, esquinas o texturas. <br>
    2. Reduce el tamaño de la imagen reteniendo solo los datos más importantes, ahorrando cómputo. <br>
    3. Toma las características detectadas, las convierte en una lista continua y toma la decisión final de clasificación. <br>
    4. Apaga neuronas al azar durante el entrenamiento para evitar que la red dependa de unos pocos nodos y cree sobreajuste. <br>
  └──── <br>


9 Pregunta 8 — Capas bajas vs capas altas <br>
═════════════════════════════════════════ <br>

  1. ¿Qué suelen captar las primeras capas de una CNN frente a las más
     profundas? <br>
  2. Usa una analogía (lupas, detectores, “de simple a complejo”). <br>
  3. ¿Por qué “poner más capas” no garantiza mejor modelo? <br>
<br>

9.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    1. Las primeras capas ven cosas simples (líneas, bordes); las capas profundas ven cosas complejas (ojos, rostros o caracteristicas completas). <br>
    2. <br>
  └──── <br>


10 Pregunta 9 — Análisis: elige arquitectura <br>
════════════════════════════════════════════ <br>

  Elige *Perceptrón (o lineal simple)* / *MLP* / *CNN* y justifica en
  *una* frase: <br>

  1. Tabla de alumnos: promedio, faltas, horas de estudio → ¿aprueba? <br>
  2. Clasificar el color de un semáforo en una fotografía. <br>
  3. Clases en el plano que *no* se separan con una recta. <br>
  4. ¿Usarías CNN para autocompletar código o una secuencia larga de 
     texto? ¿Sí/no y qué alternativa del curso mencionarías? <br>
<br>

10.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    a <br>
  └──── <br>


11 Pregunta 10 — Análisis: mirada de proyecto <br>
═════════════════════════════════════════════ <br>

  1. Train accuracy altísima y validation baja: ¿qué sospechas? ¿Qué dos
     preguntas le harías al equipo en la defensa? <br>
  2. ¿Por qué más neuronas o más capas no sustituyen un buen
     planteamiento del problema y buenos datos? <br>
  3. Escribe *tres* preguntas orales (tuyas) para verificar que
     distinguen perceptrón, MLP y CNN. <br>
<br>

11.0.1 Respuesta <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  ┌──── <br>
    a <br>
  └──── <br>
