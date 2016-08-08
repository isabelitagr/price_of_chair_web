import os

DEBUG = True
ADMINS = frozenset([
    os.environ.get("MAIL")
])  # los conjuntos frizados no pueden modificarse. no puede agregarse ni scarse info minetras la ap este corriendo

