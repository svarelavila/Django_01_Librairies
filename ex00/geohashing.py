import sys
import antigravity  # Este módulo es una broma y abre un navegador web de cómic.


def geohashing():
    """
    Computes the geohash using latitude, longitude,
    and a Dow opening value.
    """
    if len(sys.argv) != 4:
        print('Error: Exactly 3 arguments are required (latitude, longitude, datedow).')
        sys.exit(1)

    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        datedow = sys.argv[3]
    except ValueError:
        print('Usage: python3 geohashing.py 43.1496 -2.7207 2024-09-01-2041')
        sys.exit(1)

    # Validar formato de datedown
    if len(datedow.split('-')) != 4:
        print('Error: datedow must be in the format YYYY-MM-DD-xxxx')
        sys.exit(1)

    # Codifique la cadena antes de pasarla a antigravity.geohash
    encoded_datedow = datedow.encode('utf-8')

    # Llamar a la función geohash desde antigravedad
    try:
        antigravity.geohash(latitude, longitude, encoded_datedow)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    geohashing()
