from sklearn.tree import DecisionTreeClassifier

class ArbolDecision:

    def __init__(self):
        self.modelo = DecisionTreeClassifier(
            max_depth=3,
            random_state=42
        )

        self.entrenado = False

    def entrenar(self, datos):

        if len(datos) < 20:
            print("No hay suficientes datos para entrenar.")
            return False

        X = []
        y = []

        for velocidad, distancia, salto in datos:

            X.append([
                velocidad,
                distancia
            ])

            y.append(salto)

        # Verificar que existan las dos decisiones
        if len(set(y)) < 2:

            print(
                "Se necesitan ejemplos de saltar "
                "y no saltar."
            )

            return False

        self.modelo.fit(X, y)

        self.entrenado = True

        print("Arbol de decision entrenado.")
        print("Cantidad de datos:", len(datos))

        return True

    def predecir(self, velocidad, distancia):

        if not self.entrenado:
            return 0

        resultado = self.modelo.predict(
            [[velocidad, distancia]]
        )

        return int(resultado[0])