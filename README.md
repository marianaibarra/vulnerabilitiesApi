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

```bash
docker run --env-file .env -p <AVAILABLE_PORT>:8000 vulnerabilities_api:latest
```

---

# Arquitectura Cloud

Se utilizó el proveedor Google Cloud Platform para desplegar la plataforma

**Enlace:** [Url API](https://vulnerabilities-api-561467256431.us-central1.run.app)

![Architecture](/images/architecture.png)

# Reto

🔹 1. ¿Cuáles son las 3 compañías con más grupos bajo su gestión?
Hint: Usa annotate(), Count() y ordena los resultados.

🔹 2. Encuentra todos los idols que sean líderes de sus grupos.
Su position debe contener "Leader".
La consulta debe devolver el stage_name y el grupo.
Hint: Usa filter(Q(...)).

🔹 3. ¿Cuáles son los idols con la mayor diferencia entre altura y peso?
Ordena los resultados mostrando stage_name, height_cm - weight_kg.
Hint: Usa F() y annotate().

🔹 4. ¿Cuál es la duración promedio de las canciones por grupo?
Devuelve el nombre del grupo y el Avg(duration_seconds).
Hint: Usa annotate(Avg(...)).

🔹 5. Obtén todos los grupos que debutaron antes de 2010 y aún tienen al menos 5 miembros.
Hint: Filtra por debut_year y usa annotate(Count(...)).

🔹 6. Encuentra las 3 canciones más populares basadas en el número de fans que las tienen en su lista de favoritas.
Hint: Usa annotate(Count("fans")) y order_by('-count').

🔹 7. ¿Cuántos idols hay por cada compañía?
Hint: Agrupa usando values() y annotate(Count(...)).

🔹 8. ¿Qué idols tienen el mismo nombre real?
Devuelve name y la cantidad de veces que aparece.
Hint: Usa annotate(Count('id')).filter(count\_\_gt=1).

🔹 9. Encuentra los fans que tienen como favoritos al menos un idol y un grupo de la misma empresa.
Hint: Cruza datos entre favorite_idols**company y favorite_groups**company.

🔹 10. Obtén los grupos con más de 3 álbumes y al menos un título lanzado en los últimos 5 años.
Hint: Usa annotate(Count("albums")) y filtra por release_date\_\_gte.
