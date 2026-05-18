# Read & Earn — Backend (Django + MySQL)

## Requisitos previos
- Python 3.11 o superior instalado
- MySQL instalado y corriendo (puedes usar XAMPP o MySQL Workbench)
- PyCharm instalado

---

## 1. Crear la base de datos en MySQL

Abre MySQL Workbench (o la consola de MySQL) y ejecuta:

```sql
CREATE DATABASE readnearn_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 2. Abrir el proyecto en PyCharm

1. Abre PyCharm → **File → Open** → selecciona la carpeta `backend_readnearn`
2. PyCharm te pedirá crear un entorno virtual → acepta (o crea uno tú: **File → Settings → Python Interpreter → Add**)

---

## 3. Instalar las dependencias

En la terminal de PyCharm:

```bash
pip install -r requirements.txt
```

---

## 4. Crear el archivo .env

En la raíz del proyecto crea un archivo llamado `.env` (cópialo de `.env.example`):

```
SECRET_KEY=una-clave-larga-cualquiera-ponla-aqui
DEBUG=True
DB_NAME=readnearn_db
DB_USER=root
DB_PASSWORD=tu_contraseña_de_mysql
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

## 5. Crear las tablas en la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Crear un superusuario para el panel de administración

```bash
python manage.py createsuperuser
```

Te pedirá email, nombre y contraseña.

---

## 7. Arrancar el servidor

```bash
python manage.py runserver
```

El backend estará en: **http://127.0.0.1:8000**
El panel de admin en: **http://127.0.0.1:8000/admin**

---

## Endpoints disponibles

| Método | URL | Descripción | ¿Necesita token? |
|--------|-----|-------------|-----------------|
| POST | /api/registro/ | Crear cuenta | No |
| POST | /api/login/ | Iniciar sesión | No |
| GET | /api/perfil/ | Ver mi perfil | Sí |
| GET | /api/biblioteca/ | Ver mis libros | Sí |
| POST | /api/biblioteca/ | Agregar libro | Sí |
| PATCH | /api/biblioteca/{id}/ | Actualizar progreso | Sí |
| DELETE | /api/biblioteca/{id}/ | Eliminar libro | Sí |
| GET | /api/logros/ | Ver logros | Sí |
| POST | /api/logros/{id}/desbloquear/ | Desbloquear logro | Sí |
| GET | /api/premios/ | Ver premios | No |
| POST | /api/premios/{id}/canjear/ | Canjear premio | Sí |

---

## Cómo usar el token en las peticiones

Tras hacer login recibirás un `token`. Para los endpoints que necesitan autenticación, 
el frontend de Angular debe enviarlo en la cabecera de la petición así:

```
Authorization: Bearer <token>
```

---

## Tablas que se crean en MySQL

- `users` — Usuarios registrados
- `biblioteca` — Libros de cada usuario
- `logros` — Logros disponibles
- `logros_usuario` — Qué logros tiene cada usuario
- `premios` — Premios canjeables
- `canjes` — Historial de canjes
