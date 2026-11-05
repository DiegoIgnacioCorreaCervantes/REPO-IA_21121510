          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
             10 PREGUNTAS REDES NEURONALES CONVOLUCIONALES
                                 (CNN)

                            Eduardo Alcaraz
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Índice <br>
────── <br>

1. Instrucciones (alumnos) <br>
2. Pregunta 1 — Convolución a mano (3×3) <br>
3. Pregunta 2 — Contar pesos <br>
4. Pregunta 3 — ¿Qué cambia si meto más capas? <br>
5. Pregunta 4 — Formas: de volumen a vector <br>
6. Pregunta 5 — Softmax y el error “casi seguro” <br>
7. Pregunta 6 — Padding, stride y “se me achicó la imagen” <br>
8. Pregunta 7 — Dropout: ¿dónde y para qué? <br>
9. Pregunta 8 — Diseño: 5 clases de animales <br>
10. Pregunta 9 — CNN vs MLP vs RNN (mismo problema, mala herramienta) <br>
11. Pregunta 10 — Experimento mental: mover un gato <br>
12. Autoevaluación rápida (opcional) <br>
13. Notas al pie (fórmulas útiles — no sustituyen el razonamiento) <br>
<br>

1 Instrucciones (alumnos) <br>
═════════════════════════ <br>

  • Responde *con lápiz y papel* (o en este mismo buffer de Org). <br>
  • No basta con definir de memoria: hay que *calcular*, *comparar* o 
    *justificar*. <br>

<br>
2 Pregunta 1 — Convolución a mano (3×3) <br>
═══════════════════════════════════════ <br>
<br>

  Tienes este trozo de imagen en escala de grises (un canal) y este
  kernel: <br>

```
  ┌──── 
  │   Imagen 5×5                 Kernel 3×3 
  │   0  0  1  0  0              1  0 -1    
  │   0  1  2  1  0              1  0 -1    
  │   1  2  3  2  1              1  0 -1
  │   0  1  2  1  0
  │   0  0  1  0  0
  └────

resultado:
  ┌────         
  │   1  3  0  3  1              
  │   3  5  0  5  3                
  │   4  6  0  6  4                
  │   3  5  0  5  3
  │   1  3  0  3  1
  └────
```

<br>
2.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. Con *stride = 1* y *padding valid* (sin relleno), ¿cuál es el
     tamaño del mapa de salida? <br>
       N - K + 1 = Tamaño de Salida <br>
       5 - 3 + 1 = 3 <br>
       El tamaño del mapa de salida es de 3X3 <br>

  2. Calcula *solo* el valor de la esquina superior izquierda del mapa
     (la primera posición del filtro). Muestra la suma de productos. <br>

```
       0 0 1     1 0 -1
       0 1 2  *  1 0 -1  -->  0+0-1+0+0-2+1+0-3 = -5
       1 2 3     1 0 -1
```  

  1. ¿Este kernel parece detectar bordes *verticales* u *horizontales*?
     Justifica mirando los signos. <br>
       verticales, ya que la primer columna tiene solo números positivos y la segunda números negativos <br>
     <br>

3 Pregunta 2 — Contar pesos <br>
═══════════════════════════ <br>

  Una imagen RGB de *28×28×3*. Compara dos modelos: <br>

  • *Modelo A (MLP ingenuo):* aplastas la imagen a un vector y conectas 
    *todas* las entradas a una capa densa de *64 neuronas* (sin bias por 
    ahora). <br>

  • *Modelo B (CNN):* una `Conv2D' con *16 filtros* de *3×3*,
    `padding''same'=, sobre la misma imagen (con bias: un bias por
    filtro). <br>

<br>
3.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. ¿Cuántos pesos tiene la capa densa del Modelo A? (fórmula y número) <br>
     28 * 28 * 3 = 2352 entradas <br>
       Entradas X neuronas --> 2352 * 64 = 150,528 pesos <br>

  2. ¿Cuántos parámetros tiene la Conv2D del Modelo B? (pesos de kernels
     *+* biases) <br>
    
       (Kh * Kw * Cin * Cout) + Cout --> (3 * 3 * 3 * 16)+16 = 432+16 = 448 parámetros
    <br>
  3. En *una frase*: ¿por qué la CNN suele generalizar mejor con el
     mismo número de imágenes de entrenamiento? <br>
       La CNN generaliza mejor porque permite extraer patrones visuales independientemente de su posición en la 
       imagen, lo que reduce el sobreajuste. <br>

<br>
4 Pregunta 3 — ¿Qué cambia si meto más capas? <br>
═════════════════════════════════════════════ <br>
<br>

  Parte del notebook `CNNriesgo' (simplificado): <br>

```
  ┌────
  │   Entrada (21×28×3)
  │     → Conv2D(32, 3×3, same) + LeakyReLU
  │     → MaxPool(2×2)
  │     → Flatten → Dense(32) → Dense(nClasses, softmax)
  └────
```

  Quieres *apilar un segundo bloque* convolucional *antes* del Flatten: <br>

```
  ┌────
  │   … → Conv2D(32) → Pool → Conv2D(64, 3×3, same) → Pool → Flatten → …
  └────
```

<br>

4.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. Tras el *primer* MaxPool(2×2) con padding same sobre 21×28, ¿qué
     tamaño aproximado (alto×ancho) esperas? (puedes redondear / usar la
     regla “casi la mitad”) <br>
       El tamaño del mapa de características resultante es de 11 X 14 <br>

  2. ¿Qué *significan* ahora los 64 filtros de la segunda Conv2D:
     detectan bordes “crudos” o patrones *más compuestos*? Explica con
     la analogía de la lupa / capas abstractas. <br>
       Las redes convolucionales funcionan de forma jerárquica; las primeras capas capturan rasgos básicos (bordes, esquinas), 
       mientras que las capas más profundas combinan esos rasgos para reconocer partes complejas del objeto. <br>

  3. Riesgo: si añades *muchas* capas Conv+Pool con pocas imágenes, ¿qué
     falla típico verías en las curvas train vs validation? ¿Qué harías
     primero para mitigarlo (Dropout, más datos, menos filtros…)? Elige
     *una* medida y justifica. <br>
       Se produce sobreajuste (overfitting). Esto se manifiesta en las curvas cuando el error (loss) en el conjunto de entrenamiento sigue bajando, pero el error en el conjunto de validación se estanca o empieza a subir. <br>
       
       Como medida de mitigación se puede utilizar Dropout (o incorporar más datos). El Dropout apaga neuronas aleatoriamente durante el entrenamiento, evitando que un modelo tan profundo memorice las imágenes de entrenamiento y obligándolo a generalizar mejor. <br>

<br>
5 Pregunta 4 — Formas: de volumen a vector <br>
══════════════════════════════════════════ <br>
<br>
  Supón que, justo antes del Flatten, el tensor tiene forma `(7, 7, 64)'
  (lote omitido: una sola imagen). <br>
<br>

5.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ 

  1. ¿Cuántos números salen del Flatten? (un solo entero) <br>
       Al aplanar un tensor con forma (7, 7, 64), se multiplican todas sus dimensiones:
       7*7*64 = 3,136 números <br>

  2. Si la siguiente Dense tiene *32 neuronas* (con bias), ¿cuántos
     parámetros tiene *esa* Dense? <br>
       (Entradas * Neuronas) + Neuronas(incluyendo el sesgo/bias) <br>
       (3136*32)+32 = 100,384 parametros <br>

  3. Si en vez de Flatten usas *Global Average Pooling* (un promedio por
     canal), ¿qué forma tendrías a la salida y cuántos valores serían?
     ¿Ventaja frente a Flatten cuando la imagen de entrada es más
     grande? <br>
       Al calcular un promedio espacial por cada canal, la salida pasa a tener una forma de (64,), lo que equivale a un 
       total de 64 valores. <br>

       La ventaja frente a Flatten es que se reduce de forma masiva el número de parámetros en las capas densas posteriores, 
       lo que ayuda a combatir el sobreajuste y hace que la red sea independiente del tamaño de la imagen de entrada 
       (permite procesar imágenes más grandes sin que cambie el tamaño del vector resultante). <br>

<br>
6 Pregunta 5 — Softmax y el error “casi seguro” <br>
═══════════════════════════════════════════════ <br>
<br>
  Una CNN de 3 clases (inundación, incendio, tornado) saca logits que,
  tras softmax, dan: <br>

```
  ┌────
  │   P = [0.10, 0.05, 0.85]
  └────
```

  La etiqueta verdadera (one-hot) es `[0, 1, 0]' (incendio). <br>

<br>
6.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. ¿Qué clase predice el modelo (`argmax')? <br>
       Predice la tercera clase Tornado ya que 0.85 es la probabilidad más alta. <br> 

  2. ¿Está “seguro” o “confundido”? Usa los números, no adjetivos
     vacíos. <br>
       Le asigna un 85% ($0.85$) de probabilidad a una clase errónea (Tornado), mientras que a la clase real (Incendio) solo le 
       otorga un 5% ($0.05$) de probabilidad. Por lo que el modelo esta seguro de que su prediccion incorrecta es cierta. <br>

  3. Sin calcular la fórmula exacta: argumenta si la *categorical
     crossentropy* de este ejemplo será *alta* o *baja*, y por qué
     (pista: castiga cuando la probabilidad de la clase correcta es
     pequeña). <br>
       La pérdida será muy alta.La entropía cruzada categórica evalúa la fórmula ln(Pcorrecta). Como la probabilidad asignada a la clase correcta es sumamente pequeña (Pincendio = 0.05), el logaritmo de un número cercano a cero genera un valor de pérdida muy grande, penalizando fuertemente la confianza equivocada del modelo. <br>

<br>
7 Pregunta 6 — Padding, stride y “se me achicó la imagen” <br>
═════════════════════════════════════════════════════════ <br>
<br>

  Entrada *32×32*, kernel *5×5*, *un* filtro, un canal. <br>

<br>
7.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  Completa la tabla (escribe el alto×ancho de salida): <br>

```
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
   padding  stride  salida (alto×ancho) 
  ──────────────────────────────────────
   valid         1    (32-5)/1 + 1 = 27 + 1 = 28 X 28                  
   valid         2    (32-5)/2 + 1 = 27/2 + 1 = 13 + 1 = 14 X 14                 
   same          1    Mantiene originales  32 X 32                
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

  Luego: si encadenas *tres* MaxPool(2×2) seguidos sobre una imagen
  32×32 (sin cuidar bordes), ¿qué problema práctico aparece para
  clasificar objetos *pequeños* o detalles finos? <br>
    Si aplicas tres reducciones sucesivas de MaxPool(2×2), las dimensiones espaciales se reducen drásticamente: <br>
    32 X 32 --> 16 X 16 --> 8 X 8 --> 4 X 4. <br>
    Lo que hace que se pierda por completo la resolución espacial y los detalles finos. <br>
    Para clasificar objetos pequeños, el tamaño final del mapa de características se vuelve tan diminuto que el objeto pequeño 
    desaparece, se difumina o carece de suficientes píxeles para ser distinguido, haciendo imposible localizarlo o clasificarlo
    correctamente. <br>

<br>
8 Pregunta 7 — Dropout: ¿dónde y para qué? <br>
══════════════════════════════════════════ <br>
<br>

  En `CNNriesgo' hay `Dropout(0.5)' después del pooling y otra vez antes
  de la salida. <br>

<br>
8.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. Durante *entrenamiento*, ¿qué hace Dropout(0.5) en una capa densa
     de 32 neuronas (en promedio cuántas “sobreviven” por paso)? <br>
       En promedio sobrenviven 16 neuronas por cada iteración. <br>

  2. Durante *inferencia* (`predict'), ¿se apagan neuronas al azar? ¿Por
     qué sí o no? <br>
       No. Durante la inferencia se busca utilizar toda la capacidad aprendida por la red para obtener la predicción más precisa 
       y determinista posible. En lugar de desactivar neuronas, las salidas de la capa se escalan (o se usan todos los pesos ya 
       ajustados durante el entrenamiento) para compensar que ahora todas las neuronas están activas al mismo tiempo. <br>

  3. Un compañero pone Dropout *solo* en la última época “para que no se
     sobreajuste al final”. ¿Tiene sentido? Critica la idea en 3–5
     líneas. <br>
       No tiene sentido pues el propósito de Dropout es actuar como una técnica de regularización durante todo el proceso de 
       aprendizaje para obligar a la red a no depender de co-adaptaciones complejas ni memorizar el ruido de los datos. Si se 
       activa únicamente en la última época, los pesos ya habrán sufrido sobreajuste en las épocas previas. <br>

<br>
9 Pregunta 8 — Diseño: 5 clases de animales <br>
═══════════════════════════════════════════ <br>
<br>

  Debes adaptar `CNNriesgo' a: ranas, arañas, monos, ballenas, pájaros. <br>

<br>
9.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. ¿Cuántas neuronas debe tener la *última* Dense y qué activación?
     ¿Por qué? <br>
       5 neuronas(1 por clase) con activacion softmax. <br>
       Como se trata de un problema de clasificación multiclase donde cada imagen pertenece a una sola categoría exclusiva, la 
       función Softmax convierte los logits de salida en una distribución de probabilidades que suman 1. <br>

  2. Si todas las fotos entran a *224×224×3* pero el modelo tiene
     `input_shape=(21,28,3)', ¿qué *debe* pasar antes del `fit'? (una
     frase operativa) <br>
       Es necesario redimencionar todas las imagenes de entrada a 21 X 28 pixeles para que coincidan con la forma que espera el 
       modelo. <br>

  3. Propón *una* mejora de arquitectura (segundo Conv, BatchNorm, data
     augmentation…)  y di *qué síntoma* en train/val te haría pensar que
     esa mejora era necesaria. <br>
       Implementar Data Augmentation (aumento de datos con giros, zooms y traslaciones aleatorias). <br>
       El sintoma podria ser ver una brecha muy grande entre las curvas de entrenamiento y validación donde la precisión en 
       entrenamiento llega casi al 100% mientras que en validación se queda baja o empieza a empeorar. <br>

<br>
10 Pregunta 9 — CNN vs MLP vs RNN (mismo problema, mala herramienta) <br>
════════════════════════════════════════════════════════════════════ <br>
<br>

  Tres escenarios. Elige *CNN*, *MLP* o *RNN/Transformer* y justifica en
  *una* frase cada uno: 

  1. Predecir si un alumno aprueba con promedio, faltas y horas de
     estudio (tabla). <br>
       MLP: Al tratarse de datos tabulares estructurados sin propiedades espaciales o secuenciales complejas, una red densa es la opción adecuada para combinar variables independientes. <br>

  2. Clasificar fotos de semáforo (rojo / amarillo / verde). <br>
       CNN: Al trabajar con imágenes, aprovecha la estructura bidimensional y los filtros locales para reconocer patrones visuales sin importar su posición exacta. <br>

  3. Autocompletar la siguiente línea de código dado el prefijo escrito. <br>
       RNN / Transformer: El código es una secuencia de texto donde el orden cronológico y el contexto de las palabras anteriores determinan lógicamente el siguiente token. <br>

  Si aplastas la foto del semáforo y usas un MLP “grande”, ¿puede
  *aprender*? ¿Qué sacrificas respecto a una CNN? (parámetros, datos,
  invariancia…) <br>
    Sí, un MLP con suficientes neuronas y parámetros es capaz de aproximar funciones complejas y aprender a clasificar las 
    imágenes mediante fuerza bruta si cuenta con datos suficientes. <br>
    Parametros: Dispara el número de pesos de forma desproporcionada, haciendo el modelo mucho más pesado. 
    Datos: Requiere una cantidad masiva de imágenes de entrenamiento adicionales para evitar el sobreajuste
    invariancia: Destruye la vecindad local de los píxeles al aplanar la imagen; si el semáforo cambia levemente de lugar en la 
    foto, el MLP fallará porque ya no sabrá mapear esa posición relativa, algo que la CNN resuelve de manera natural gracias a 
    la compartición de pesos. <br>

<br>
11 Pregunta 10 — Experimento mental: mover un gato <br>
══════════════════════════════════════════════════ <br>
<br>

  Entrenaste una CNN que detecta “hay un gato” en fotos 64×64. En el
  test, el mismo gato aparece *corrido 10 píxeles a la derecha*, mismo
  fondo, misma escala. <br>

<br>
11.0.1 Tareas <br>
╌╌╌╌╌╌╌╌╌╌╌╌╌ <br>

  1. ¿Por qué una CNN tiene *más chance* de seguir acertando que un MLP
     que ve el vector aplastado? (pesos compartidos / detección local) <br>
       Debido a la detección local y a la compartición de pesos. El filtro de la CNN se desliza por toda la imagen buscando el 
       patrón del gato sin importar en qué posición exacta esté, mientras que el MLP asocia cada neurona a una posición fija del 
       vector aplastado, por lo que mover el gato altera todos los valores de entrada. <br>

  2. Si en vez de correrlo lo *giraras 90°* y nunca viste gatos de lado
     en el train, ¿la CNN “mágica” garantiza acierto? ¿Qué haría falta
     (augmentation, más datos…)? <br>
       No, la CNN no garantiza el acierto. Aunque la CNN maneja traslaciones locales, no es automáticamente invariante a rotaciones drásticas de 90° si nunca ha visto ejemplos similares. Para solucionarlo, haría falta aplicar data augmentation (aumento de datos con rotaciones) o incorporar más datos de entrenamiento que incluyan gatos orientados de esa forma. <br>

  3. Escribe *una* pregunta que tú le harías a un compañero para
     comprobar si entendió qué son los *pesos del kernel* (no copies las
     de arriba). <br>
       Si un kernel detecta una característica específica y duplicamos el valor numérico de todos sus pesos, ¿qué pasará con la 
       magnitud de los valores en el mapa de características resultante? <br>
       

<br>
12 Autoevaluación rápida (opcional) <br>
═══════════════════════════════════ <br>
<br>
  Marca 1–5 (1 = no entendí, 5 = lo explicaría en pizarrón): <br>

```
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
   Tema                                Nota 
  ──────────────────────────────────────────
   Producto punto del kernel                
   Conteo de parámetros Conv vs Dense       
   Efecto de apilar Conv+Pool               
   Softmax + pérdida                        
   Dropout train vs inferencia              
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

13 Notas al pie (fórmulas útiles — no sustituyen el razonamiento) <br>
═════════════════════════════════════════════════════════════════ <br>
<br>
  • Salida convolución (un eje), padding valid: \(\lfloor (N - K)/S
    \rfloor + 1\) <br>
  • Padding same + stride 1: salida ≈ mismo \(N\) <br>
  • Parámetros Conv2D: \(K_h \cdot K_w \cdot C_{in} \cdot C_{out} +
    C_{out}\) (si hay bias) <br>
  • Parámetros Dense: \(n_{in} \cdot n_{out} + n_{out}\) (si hay bias) <br>
