import sys
import antigravity


def geohash():
    # Validar número de argumentos
    if len(sys.argv) != 4:
        print("Usage: python geohashing.py <latitude> <longitude> <date>")
        sys.exit(1)  # Importante para que el script no continúe ejecutándose

    try:
        # Extraer y convertir argumentos
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        date = sys.argv[3].encode()  # Codificar la fecha como bytes para antigravity

        # Calcular el geohash
        antigravity.geohash(latitude, longitude, date)

    except ValueError as e:
        # Manejo de errores de conversión
        print(f"Error: Invalid input format. {e}")
        sys.exit(1)
    except Exception as e:
        # Manejo de cualquier otro error inesperado
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    geohash()
