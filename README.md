# Vulnerabilities API

---

## Uso local

1. Clona el repositorio

```bash
git clone https://github.com/marianaibarra/vulnerabilitiesApi.git
```

2. Crea un entorno virtual

```bash
cd project_directory
python -m venv .env
pip install -r requirements.txt
```

3. Configura las variables de entorno de la base de datos en un archivo .env

```.env
NAME=vulnerabilities
DB_USER=
PASSWORD=
HOST=
PORT=5432
```

4. Arranca la aplicación

```bash
python manage.py runserver
```

### Con docker

1. Crea la imagen

```bash
docker build . -t vulnerabilities_api -f Dockerfile
```

2. Ejecuta el contenedor pasando las variables de entorno

``` bash
docker run --env-file .env -p <AVAILABLE_PORT>:8000 vulnerabilities_api:latest
```

---

# Arquitectura Cloud

Se utilizó el proveedor Google Cloud Platform para desplegar la plataforma

**Enlace:** [Url API](https://vulnerabilities-api-561467256431.us-central1.run.app)

![Architecture](/images/architecture.png)