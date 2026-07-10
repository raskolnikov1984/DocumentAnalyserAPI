from invoke import task


@task
def run(c):
    """Run API en desarrollo con hot-reload."""
    c.run("uvicorn app.main:app --reload", pty=True)


@task(
    iterable=["path"],
    help={"path": "Ruta especifica de test (ej: tests/unit/test_validators.py)"},
)
def test(c, path=None):
    """Ejecutar tests."""
    target = " ".join(path) if path else ""
    c.run(f"pytest -v {target}", pty=True)


@task
def build(c):
    """Construir imagenes Docker."""
    c.run("docker compose build")


@task
def deploy(c):
    """Desplegar en produccion con Docker Compose."""
    c.run("docker compose up -d --build")


@task
def stop(c):
    """Detener servicios Docker Compose."""
    c.run("docker compose down")


@task
def logs(c):
    """Ver logs en tiempo real."""
    c.run("docker compose logs -f", pty=True)


@task
def migrate(c):
    """Ejecutar migraciones pendientes de la base de datos."""
    c.run("alembic upgrade head", pty=True)


@task
def migration(c, message):
    """Crear una nueva migracion autogenerada."""
    c.run(f'alembic revision --autogenerate -m "{message}"', pty=True)
