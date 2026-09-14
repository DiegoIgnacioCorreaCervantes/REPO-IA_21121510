## Actividad Dino Crash EDA conceptual <br>

**Analista:** [Diego Ignacio Correa Cervantes / 21121510]

### Bloque 1 — ¿Qué dataset necesitamos? <br>

#### Misión 1: Definir el problema y el dataset ideal <br>

*Escenarios posibles* <br>

![ImagenB1_1](imagenesMD/dinorunB1.png) <br></br>

*P1*

+ Variable objetivo (Y): Nombre de la columna *morirá?*, tipo binaria ya que es una respuesta de si o no.
+ Variables de entrada (X): esta vivo?, Numero de frame, velocidad del dinosaurio, tiempo, distancia desde el obstaculo anterior, distancia hasta el siguiente obstaculo, ¿esta saltando?, ¿esta agachado?, tipo del obstaculo anterior, tipos de obstaculos.
+ Granularidad: Necesita revisarse cada vez que el dinosaurio avance un frame dentro de la partida para evaluar si morira en el siguiente, al final  de la partida se obtendra la informacion del ultimo frame evaluado.
+ Tamaño mínimo razonable: Suficientes partidas para abarcar todos los casos en los que el dinosaurio puede morir al avanzar al siguiente frame.
+ Riesgo si el dataset está mal definido: no abarcar datos sufuientes para distinguir cuando es que el dinosaurio puede morir, no podra evaluarse correctamente cuando puede morir el dinosaurio y por lo tanto no se aprendera como evitarlo. <br>

*P2*

+ Variable objetivo (Y): Nombre de la columna *puntaje*, tipo numérica/entero pues es un valor que crece conforme mas tiempo dure una partida.
+ Variables de entrada (X): Numero de frame, tiempo, velocidad del dinosaurio, numero de obstaculos superados, distancia en frames recorrida. 
+ Granularidad: Se requiere de un registro que actualice los datos con cada frame recorrido y arroje un resumen al final de la partida.
+ Tamaño mínimo razonable: Una partida completa pues se trata de la puntuacion al final de la partida en curso.
+ Riesgo si el dataset está mal definido: No establecer una forma o formula de como calcular el puntaje, no sera posible calcular el puntaje al final de la partida lo que hara mas dificil distinguir las diferencias de cada una para aprender cual es un resultado deseable. <br>

*P3*

+ Variable objetivo (Y): Nombre de la columna *Tipo del siguiente obstaculo*, tipo categórica pues existen varios tipos de obstaculos. 
+ Variables de entrada (X): numero de frame, velocidad del dinosaurio, tiempo, distancia desde el obstaculo anterior, distancia hasta el siguiente obstaculo, tipo del obstaculo anterior, tipos de obstaculos. 
+ Granularidad: se requiere revisar cada vez que se avance un frame durante la partida para poder evaluar si viene un obstaculo y de que tipo es.   
+ Tamaño mínimo razonable: las partidas necesarias para empezar a predecir que tan seguido pueden aparecer y de que tipo son los obstaculos.   
+ Riesgo si el dataset está mal definido: La informacion sobre los obstaculos no esta bien diferenciada, se produciran datos erroneos que volveran imposible crear predicciones utiles <br></br> 

#### Misión 2: Diccionario de datos (qué debe traer el CSV) <br>

*Borrador para P1* <br>

![ImagenB1_2](imagenesMD/dinorunB1_2.png) <br></br> 

*Preguntas:* <br>

1. ¿Qué patrón ves en la fila donde died=1 (frame 82)? <br>
   El dinosaurio a avanzado y frente a el se encuentra un cactus pequeño que no logro saltar por lo cual la partida termino. <br>

2. ¿=score= es buena variable para predecir muerte en el siguiente frame? ¿Por qué sí o no? <br>
   No es tan exacta como la variable tiempo_ms pero ambas pueden servir para saber que tanto a durado la partida y mientras mas dure es mas probable que no sea posible sortear algun obstaculo. <br>

3. ¿Falta alguna columna crítica para P1? (pista: altura del dino, agachado, lag de reacción del jugador…) <br>
   ancho del dinosaurio, largo del dinosaurio, esta agachado?, tiempo de reaccion del jugador, distancia desde el obstaculo anterior. 

4. ¿=died= tal como está definida sirve para P1 o solo describe el final de la partida? <br>
   Describe el final de la partida lo que ayuda a diferenciar cada una, sin embargo tambien genera un desbalance pues siempre habra muchos menos registros de muerte. <br></br>

### Bloque 2 —  Preguntas que todo EDA debe responder <br>

#### Misión 3: Las diez preguntas del analista <br></br> 

![ImagenB1_2](imagenesMD/dinorunB2_1.png) <br></br> 

*Preguntas:* <br>

1. Elige tres preguntas del checklist y respóndelas como si tuvieras el dataset completo del dino (hipótesis razonables). <br>
   + Pregunta 3 --> ¿La clase objetivo está balanceada? (P1)<br>
     La mayoría de los frames son de "no-muerte" lo que significa que el dinosaurio vive en muchos frames antes de chocar y cambiar de estado por lo que el dataset esta fuertemente desbalanceado. <br>

   + Pregunta 6 — ¿Distribución de *speed*? <br>
     En el juego real, la velocidad aumenta progresivamente con el score pero se estabiliza en un máximo. Por lo tanto lo ideal es utilizar las variables de time_ms y score como guia para alcanzar una distribucion creciente pero no lineal e infinita. <br>
  
   + Pregunta 8 — ¿Datos i.i.d.? <br>
     Los frames consecutivos de una partida están altamente correlacionados por ejemplo el score de un frame depende del anterior,
     *speed* es acumulativa, la posición de los obstáculos es continua. Por esto los registros individuales pueden aportar informacion insuficiente a la hora de entrenar un modelo con lo cual agregar un ID para la sesion ayudaria a contemplarlos como un conjunto. 
     <br>

2. Para la pregunta 8 (i.i.d.): explica por qué mezclar frames de la misma partida en entrenamiento y prueba es un error. <br>
   Si se divide el dataset por filas sueltas (aleatoriamente), frames de la misma partida pueden terminar en sitios diferentes lo cual generara errores ya que Los frames de una misma sesión no son independientes y deben analizarse en conjunto. <br>
   
3. Da un ejemplo concreto de data leakage usando score o time_ms en P1. <br>
   El modelo podria empezar a usar el score final de la partida registrado en otras para predecir si el dinosaurio muere. Al ser el frame de muerte el que tiene el score mas alto de la tabla el modelo aprendera que "score alto = muere". En el momento real de predecir el frame *t*, no se sabe si el dinosaurio morirá en *t+1*; solo se conoce el score hasta *t*. Por lo que al usar el score final de otras partidas este estara usando información del futuro absoluto. Así cuando el dinosaurio lleve un score considerado alto y siga vivo, el modelo predecirá "va a morir" constantemente, fallando estrepitosamente. <br></br>

#### Misión 4: Leer distribuciones sin gráfica (interpretación) <br></br> 

![ImagenB1_2](imagenesMD/dinorunB2_2.png) <br></br> 

*Preguntas:* <br>

+ ¿El problema P1 (muerte en siguiente frame) está desbalanceado? Cuantifica con los números dados. <br>
  Esta desbalanceado pues de 12000 frames 50 son de muerte y 11950 de "no muerte", en porcentaje seria 0.42% y 99.58% respectivamente. <br>

+ ¿Qué implica eso para la métrica que usarías? (accuracy vs precision/recall/F1). <br>
  Gracias al desbalance no debe usarse accuracy pues es muy probable que no detecte ninguna muerte por la gran diferencia. <br>
  Precision puede medir cuántas de las muertes predichas son reales lo que evitara falsos positivos.
  Recall puede medir cuántas muertes reales detecta de forma que no se pierdan entre la gran cantidad de registros.
  F1 ofrece un balance entre precision y recall lo que lo hace bastante recomendable.

+ ¿=dist_obstacle= parece útil como predictor? Argumenta con la fila de muertes. <br>
  Si pero no por si sola, la media global *95* está muy lejos del umbral de muerte. Cuando el obstáculo está muy cerca, el dinosaurio tiene menos margen para saltar lo que se traduce en mayor probabilidad de choque. Sin embargo no es del todo exacta ya que aun a poca distancia podria haber espacio suficiente para que el dinosaurio pase el obsrtaculo.

+ ¿La distribución de score sugiere regresión simple o necesitas transformación / otro enfoque? <br>
  No se trata de una regrsión simple pues hay pocos frames con score muy alto (hasta 120), pero la mayoría se concentran en valores bajos. Lo que denota una distribucion asimétrica. Usar otro enfoque con score podria ayudar al modelo ya que al ser acumulativo este podria crear sesgos y no aportar un valor real a la predicción. <br></br>

### Bloque 3 —  Del EDA a la elección del modelo <br>

#### Misión 5: Árbol de decisión “dataset → modelo” <br></br> 

![ImagenB1_2](imagenesMD/dinorunB3_1.png) <br></br> 

*Para cada escenario del inicio:* <br>

|Escenario|Tras tu EDA, ¿qué fila de la guía aplica?|  Modelo que propondrías  |       2 condiciones del dataset que  deben cumplirse       |
|:-------:|:---------------------------------------:|:------------------------:|:----------------------------------------------------------:|
| *P1*<br>*¿Morirá en el siguiente frame?* | Y binaria muy desbalanceada | Regresión logística o Random Forest | 1. Ratio 239:1 entre clases.<br>2. Sin leakage de `score`/`time_ms`. |
| *P2*<br>*¿Cuántos puntos al morir?* | Y numérica | Regresión lineal regularizada o<br> Arbol regressor | 1. Una fila por partida agregando session_id.<br>2. Sin leakage del score final. |
| *P3*<br>*¿Qué obstáculo viene?* | Y categórica multiclase | Logística multinomial o Random Forest | 1. El target tiene 4 clases con distribucion conocida.<br>2. Sin leakage del obstáculo futuro. |

<br></br>

#### Misión 6: Contraejemplo — cuándo no usar un modelo <br>

*Preguntas* <br>

1. Describe un escenario del dinosaurio donde un árbol profundo parecería buena idea pero el EDA lo desaconsejaría. <br>
   P1 es una clasificación binaria no lineal, con interacciones complejas entre dist_obstacle, speed, jump y obstacle_type.
   Sin embargo se desaconseja usar árboles profundos por desbalance extremo (239:1), pocos positivos (50) y riesgo de leakage. Mejor árboles poco profundos con class_weight.

2. Describe un escenario donde una red neuronal tendría sentido y qué deberías ver en el EDA para justificarla. <br>
   Tendría sentido en P3 (secuencia temporal). El EDA debe mostrar: muchas sesiones, frames correlacionados, patrones no triviales, features ricas. Sin eso, es overkill.

3. ¿Se podría resolver P1 con reglas fijas (si dist_obstacle < X y jump=0 entonces muerte)? Compara con un modelo aprendido: ventajas y      límites. <br>
   La regla fija es buen baseline, interpretable y sin leakage, pero tiene umbral arbitrario, ignora speed/obstacle_type y bajo recall. El modelo aprende mejor pero requiere datos y tener cuidado con fugas.
