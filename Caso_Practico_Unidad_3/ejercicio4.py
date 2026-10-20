class AnalisisSentimiento:
    def __init__(self, palabras_positivas=None, palabras_negativas=None):
        """
        Inicializa la clase con listas predeterminadas o personalizadas de palabras.
        """
        self.palabras_positivas = palabras_positivas if palabras_positivas else ["bueno", "buena", "excelente", "gustó"]
        self.palabras_negativas = palabras_negativas if palabras_negativas else ["malo", "mala", "horrible", "pésimo"]

    def _contar_positivas(self, texto: str) -> int:
        """Método privado para contar el total de coincidencias de palabras positivas."""
        palabras_texto = texto.lower().split(' ')
        return sum([palabras_texto.count(p.lower()) for p in self.palabras_positivas])

    def _contar_negativas(self, texto: str) -> int:
        """Método privado para contar el total de coincidencias de palabras negativas."""
        palabras_texto = texto.lower().split(' ')
        return sum([palabras_texto.count(p.lower()) for p in self.palabras_negativas])

    def predict(self, texto: str) -> str:
        """
        Determina la polaridad de la opinión basándose en la comparación de conteos.
        """
        pos = self._contar_positivas(texto)
        neg = self._contar_negativas(texto)

        if pos > neg:
            return "Positiva"
        elif neg > pos:
            return "Negativa"
        else:
            return "Neutral"

    def fit(self, nuevas_positivas: list, nuevas_negativas: list):
        """
        Actualiza y amplía el vocabulario léxico del modelo.
        """
        if nuevas_positivas:
            self.palabras_positivas.extend(nuevas_positivas)
        if nuevas_negativas:
            self.palabras_negativas.extend(nuevas_negativas)
        print("[MODELO ACTUALIZADO]: Se han agregado nuevas palabras clave al léxico.")


# Pruebas del modelo de Análisis de Sentimiento
if __name__ == "__main__":
    opiniones = [
        "Me ha parecido una película muy buena",
        "La música es mala, pero la fotografía es buena",
        "No me ha gustado nada, no la recomiendo",
        "El doblaje es pésimo y la trama es muy mala",
        "Excelente película, 100% recomendable",
        "La banda sonora es maravillosa y la trama me gustó"
    ]

    # Instanciación inicial
    modelo = AnalisisSentimiento()

    print("=== PREDICCIONES CON EL MODELO INICIAL ===")
    for idx, op in enumerate(opiniones, start=1):
        prediccion = modelo.predict(op)
        print(f"Opinión {idx}: '{op}' -> Predicción: {prediccion}")

    print("\n--- Entrenando / Actualizando el modelo con método fit() ---")
    # Se incorporan palabras como "maravillosa", "recomendable", "pésimo" si no estaban
    modelo.fit(
        nuevas_positivas=["maravillosa", "recomendable"],
        nuevas_negativas=["pésimo"]
    )

    print("\n=== PREDICCIONES TRAS LA ACTUALIZACIÓN (FIT) ===")
    for idx, op in enumerate(opiniones, start=1):
        prediccion = modelo.predict(op)
        print(f"Opinión {idx}: '{op}' -> Predicción: {prediccion}")
