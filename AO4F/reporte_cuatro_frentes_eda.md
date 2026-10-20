## Actividad Operación 4 frentes <br>

**Analista:** [Diego Ignacio Correa Cervantes / 21121510]

### Misión 1: Semáforo Académico <br>

- **Pregunta de negocio:** ¿Cuál será el nivel de riesgo de reprobar de cada alumno al cierre del parcial?
- **Tipo propuesto:** Clasificar — justificación: La variable objetivo `riesgo` es categórica nominal con 3 clases (verde, amarillo, rojo). No es un número continuo, por lo que predecir una categoría es una tarea de clasificación.
- **Y / forma de Y:** `riesgo` (categórica, 3 clases: verde, amarillo, rojo). Distribución: 40% verde, 35% amarillo, 25% rojo. Está moderadamente balanceada.
- **X (mínimo 5):** 
  1. `asistencia_pct` (numérico) — Correlaciona negativamente con el riesgo (a mayor asistencia, menor riesgo).
  2. `promedio_parciales` (numérico) — Predictor directo del desempeño; a mayor promedio, menor riesgo.
  3. `tareas_entregadas` (entero) — Mide el compromiso; a más tareas, menor riesgo.
  4. `reprobadas_previas` (entero) — Historial académico; a más reprobadas, mayor riesgo.
  5. `horas_plataforma` (numérico) — Engagement; a más horas, menor riesgo.
  6. `turno` (categórico) — Variable contextual; puede haber diferencias entre matutino y vespertino.
- **Hallazgos EDA:** 
  - Las medias por clase muestran separación clara: `verde` tiene asistencia 91%, promedio 8.4 y 0.2 reprobadas; `rojo` tiene asistencia 52%, promedio 5.0 y 2.4 reprobadas. Las variables separan bien las clases.
  - No hay valores faltantes en la muestra, pero podría haberlos en el dataset completo (ej. alumnos sin parciales).
- **Leakage evitado:** No usar `alumno_id` como feature. Si se predice al cierre del parcial, `promedio_parciales` y `tareas_entregadas` son válidas porque se conocen en ese momento. Si se predijera antes, serían leakage.
- **Métricas coherentes con mi tipo:** F1-macro (trata las 3 clases por igual) y Recall de la clase `rojo` (minimizar falsos negativos: alumnos en riesgo alto no detectados).
- **Modelo propuesto y condición:** Regresión Logística Multinomial o Random Forest. Condición: las clases deben estar razonablemente representadas (lo están: 40/35/25) y sin multicolinealidad severa entre `asistencia_pct`, `tareas_entregadas` y `horas_plataforma`. <br>

### Misión 2: Alerta de Churn <br>

- **Pregunta de negocio:** ¿Este alumno abandonará la materia a mitad de semestre?
- **Tipo propuesto:** Clasificar — justificación: La variable objetivo `abandona` es binaria (0/1). Predecir si ocurre un evento (abandono) es una clasificación binaria.
- **Distribución de Y e implicaciones:** `abandona=1`: 70 casos (14%); `abandona=0`: 430 casos (86%). **Dataset desbalanceado**. Un modelo trivial que diga "nadie abandona" tendría 86% de accuracy, pero sería inútil. Implica usar métricas como F1, Recall o PR-AUC en lugar de accuracy.
- **Tratamiento de NA:** `calif_actividad_1` tiene muchos NA. Hipótesis: los alumnos que abandonan no entregaron la actividad 1. **Tratamiento:** imputar con la mediana solo si es necesario, pero mejor crear una bandera `tiene_calif = 0/1` para capturar el patrón de ausencia. No borrar filas, ya que los NA son informativos.
- **Métricas y costo de error:** 
  - **Recall (abandona=1):** Es la métrica más importante. El costo de un Falso Negativo (predecir que no abandona cuando sí lo hace) es alto: se pierde la oportunidad de intervenir.
  - **Precision:** También importa, pero menos. Un Falso Positivo (predecir abandono cuando no lo hace) genera una intervención innecesaria, que es menos costosa que perder al alumno.
- **Modelo propuesto:** Regresión Logística con `class_weight='balanced'` o Random Forest con `class_weight='balanced'`. Condición: dividir train/test de forma estratificada para mantener la proporción 86/14. <br>

### Misión 3: Pronóstico de Puntaje <br>

- **Pregunta de negocio:** ¿Qué calificación final obtendrá el alumno?
- **Tipo propuesto:** Predecir — justificación: La variable objetivo `calificacion_final` es numérica continua (0-100). Predecir un número exacto es una tarea de regresión.
- **Qué se gana/pierde si se convierte a aprobado/reprobado:** 
  - **Gana:** Simplicidad interpretativa, se convierte en clasificación binaria, más fácil de comunicar.
  - **Pierde:** Información granular. Saber que un alumno sacará 68 vs 75 es útil para tutorías personalizadas. Además, se pierde la capacidad de ordenar a los alumnos por nivel de riesgo.
- **Outliers / errores de captura:** Hay 3 filas con `calificacion_final > 100`. Es un error de captura. **Decisión:** Eliminarlas o corregirlas (si es posible). No son outliers reales, son errores.
- **Métricas (2):** 
  1. **MAE (Error Absoluto Medio):** Mide el error promedio en puntos. Fácil de interpretar (ej. "el modelo se equivoca en ±5 puntos").
  2. **RMSE (Raíz del Error Cuadrático Medio):** Penaliza más los errores grandes. Útil si un error de 20 puntos es mucho peor que dos errores de 10.
- **Modelo propuesto:** Regresión Lineal Múltiple (si hay linealidad) o Gradient Boosting Regressor (si hay no linealidad). Condición: `examen_1` y `examen_2` están altamente correlacionados (~0.85), lo que puede causar multicolinealidad en regresión lineal. Se debe evaluar eliminar una o usar regularización (Ridge). <br>

### Misión 4: Tiempo de Estudio <br>

- **Pregunta de negocio:** ¿Cuántas horas adicionales necesita un alumno para dominar el tema?
- **Tipo propuesto:** Predecir — justificación: La variable objetivo `horas_adicionales` es numérica continua (2.0, 18.0, 35.0...). Predecir un número es una tarea de regresión.
- **Hipótesis dificultad → horas:** "A mayor dificultad del tema, más horas adicionales se necesitan". Los datos lo confirman: `baja` → 3.2h media; `media` → 7.8h; `alta` → 16.5h. La relación es clara y monótona.
- **Cola larga: ¿borrar o conservar?:** El 3% de alumnos con >40h es una cola larga. **Decisión:** Conservar. Son casos reales (temas muy difíciles o alumnos con muchas dificultades). Borrarlos sesgaría el modelo hacia abajo. Se puede aplicar una transformación logarítmica a Y para manejar la asimetría.
- **Alternativa de binarizar Y:** Binarizar con umbral 15h ("tutoría intensiva: sí/no") tendría sentido si el objetivo es **decidir una acción** (asignar tutoría o no). Se pierde la granularidad de "cuántas horas exactas", pero se gana en simplicidad y accionabilidad. Se pierde la capacidad de priorizar dentro del grupo "intensivo".
- **Métricas y modelo + 2 chequeos EDA:** 
  - **Métricas:** MAE y RMSE (si se predice el número); F1 y Recall (si se binariza).
  - **Modelo:** Random Forest Regressor o Gradient Boosting (manejan bien relaciones no lineales y colas largas).
  - **Chequeo 1:** Verificar que `tema_dificultad` esté codificada correctamente (ordinal: baja < media < alta).
  - **Chequeo 2:** Revisar si `pretest_score` y `ejercicios_correctos_pct` están correlacionados (redundancia). Si lo están, eliminar una o combinarlas. <br>
  
## Síntesis <br>

1. Tabla resumen de mis cuatro propuestas de tipo (M1-M4): <br>

| Misión | Variable Objetivo (Y) | Tipo de Y | Tipo de Problema | Modelo Propuesto |
|---|---|---|---|---|
| M1 | `riesgo` | Categórica (3 clases) | Clasificación Multiclase | Logística Multinomial / Random Forest |
| M2 | `abandona` | Binaria (0/1) | Clasificación Binaria | Logística / Random Forest con `class_weight` |
| M3 | `calificacion_final` | Numérica continua | Regresión | Regresión Lineal / Gradient Boosting |
| M4 | `horas_adicionales` | Numérica continua | Regresión | Random Forest Regressor / Gradient Boosting |
<br>

2. **Pista usada para decidir "clase vs número":** Si la pregunta es "¿a qué grupo pertenece?" y Y es una etiqueta/categoría, es clasificación. Si la pregunta es "¿qué número espera?" y Y es un valor continuo, es regresión.
3. **Frase final:** "El tipo de problema se deduce de la pregunta y de Y porque la naturaleza de la variable objetivo dicta si buscamos predecir una categoría (clasificar) o un valor numérico (predecir)."
<br></br>
