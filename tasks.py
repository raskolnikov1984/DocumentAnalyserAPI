from invoke import task


@task
def run(c):
    """Run a shell command."""
    c.run("uvicorn app.main:app --reload", pty=True)
