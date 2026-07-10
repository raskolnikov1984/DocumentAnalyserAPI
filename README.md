# DocumentAnalyserAPI

API para validación e ingreso de datos CBAM (Carbon Border Adjustment Mechanism). Recibe archivos .xlsx, valida cada fila contra reglas de negocio (EORI, CN Code, país ISO, fechas, etc.), persiste registros válidos y devuelve errores detallados por fila inválida.

## Stack

- Python 3.14 + FastAPI
- SQLAlchemy 2.0 asíncrono
- SQLite (desarrollo) / PostgreSQL 18 (producción)
- openpyxl (parseo de Excel)
- Docker Compose
- Poetry (gestión de dependencias)
- Invoke (automatización de tareas)

## Requisitos

- Python >= 3.14
- Poetry
- Docker y Docker Compose (solo para producción)

## Desarrollo

```bash
# 1. Clonar e instalar dependencias
poetry install --no-root

# 2. Activar entorno virtual
poetry shell

# 3. Ver tareas disponibles
invoke --list

# 4. Ejecutar en modo desarrollo (hot-reload)
invoke run

# 5. Ejecutar tests
invoke test

# Ejecutar tests especificos
invoke test --path tests/unit/test_validators.py
invoke test --path tests/integration/test_bulk_upload.py
```

## Producción

```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores de producción (POSTGRES_PASSWORD, etc.)

# 2. Desplegar
invoke deploy

# La API queda disponible en http://localhost:18020

# Otros comandos
invoke stop    # docker compose down
invoke logs    # docker compose logs -f
```

## Tareas Invoke

| Comando | Descripción |
|---------|-------------|
| `invoke run` | Inicia servidor de desarrollo con hot-reload |
| `invoke test` | Ejecuta todos los tests |
| `invoke test --path <ruta>` | Ejecuta un test específico |
| `invoke build` | Construye imágenes Docker |
| `invoke deploy` | Despliega a producción con Docker Compose |
| `invoke stop` | Detiene servicios |
| `invoke logs` | Muestra logs en tiempo real |
