from invoke import task


@task
def run(c):
    """Run API en desarrollo con hot-reload."""
    c.run("uvicorn app.main:app --reload", pty=True)


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
    c.run("docker compose logs -f")
