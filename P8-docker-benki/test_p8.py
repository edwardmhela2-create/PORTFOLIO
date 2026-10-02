from pathlib import Path

MJI = Path(__file__).resolve().parent
P6 = MJI.parent / "P6-benki-app"


def test_dockerfile_ipo_ya_sahihi():
    d = (MJI / "Dockerfile").read_text(encoding="utf-8")
    assert "FROM python" in d
    assert "WORKDIR /app" in d
    assert "COPY P6-benki-app/" in d
    assert "pip install" in d
    assert "EXPOSE 5000" in d
    assert "CMD" in d and "app.py" in d
    assert "USER mtumiaji" in d
    assert "ENV BENKI_DB=/data/benki.db" in d
    assert "HEALTHCHECK" in d


def test_dockerfile_haina_siri():
    d = (MJI / "Dockerfile").read_text(encoding="utf-8")
    assert "secret" not in d.lower()
    assert "benki123" not in d


def test_compose_na_volume():
    c = (MJI / "docker-compose.yml").read_text(encoding="utf-8")
    assert "benki-data:/data" in c
    assert "5000:5000" in c
    assert "volumes:" in c
    assert "127.0.0.1:5000:5000" in c


def test_dockerignore_haina_db_na_project_zingine():
    d = (MJI.parent / ".dockerignore").read_text(encoding="utf-8")
    assert "*.db" in d or "**/*.db" in d
    assert "P7-cyber-toolkit" in d
    assert "P3-mkopo-cli" in d


def test_app_yasoma_env_benki_db():
    a = (P6 / "app.py").read_text(encoding="utf-8")
    assert "os.environ.get(" in a
    assert '"BENKI_DB"' in a


def test_readme_ipo():
    r = (MJI / "README.md").read_text(encoding="utf-8")
    assert "docker compose" in r
    assert "volume" in r.lower()
    assert "Container vs Virtual Machine" in r
