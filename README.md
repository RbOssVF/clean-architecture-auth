# FastAPI Clean Architecture - Super RBAC & Auth System

Este repositorio contiene una implementación robusta de un sistema de **Autenticación y Autorización (RBAC)** utilizando **FastAPI** y **SQLModel**, siguiendo los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**.

El proyecto está diseñado para ser escalable, mantenible y listo para producción, con una orquestación centralizada de transacciones, validaciones y seguridad.

## 🚀 Características Principales

- **Arquitectura Limpia**: Separación clara de responsabilidades en capas (Domain, Application, Infrastructure, Presentation).
- **Control de Acceso Basado en Roles (RBAC)**: Gestión granular de roles y permisos.
- **Super-Admin Bypass**: El permiso `admin.full_access` otorga acceso total a cualquier recurso.
- **JWT Authentication**: Sistema de tokens de acceso y refresco (Access & Refresh Tokens) con `python-jose`.
- **Orquestador Base (`BaseUseCaseHandler`)**: 
  - Gestión automática de **Transacciones** (Commit/Rollback) según el método HTTP.
  - Validación dinámica de Schemas Pydantic.
  - Control de seguridad (Auth/Roles/Permisos) antes de la ejecución del caso de uso.
- **Smart Router (`ValidadorRutasInteligentes`)**: Extensión de `APIRouter` para registrar casos de uso de forma declarativa y limpia.
- **Database**: Uso de **SQLModel** para una integración perfecta entre modelos de base de datos y validaciones de Pydantic.

---

## 🏗️ Estructura del Proyecto

```text
├── app/
│   ├── users/                 # Módulo de Usuarios
│   │   ├── application/       # Servicios, DTOs y Casos de Uso
│   │   ├── domain/            # Entidades, Repositorios (Interfaces) y Excepciones
│   │   ├── infrastructure/    # Modelos SQLModel y Repositorios (Implementación)
│   │   └── presentation/      # Rutas (Endpoints) y Schemas Pydantic
│   ├── roles/                 # Módulo de Roles y Permisos (Estructura similar)
├── shared/                    # Núcleo del Framework
│   ├── base.py                # BaseUseCaseHandler, Mixins de Transacción y Auth
│   ├── database.py            # Configuración de Engine y Manejo de Sesiones
│   ├── security/              # Servicio JWT
│   └── utils.py               # Utilidades globales (Timezone, etc.)
├── main.py                    # Punto de entrada de la aplicación
└── requirements.txt           # Dependencias del proyecto
```

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web de alto rendimiento.
- **SQLModel**: Combinación de SQLAlchemy y Pydantic.
- **PostgreSQL**: Base de datos recomendada (psycopg2-binary).
- **Python-Jose**: Para la gestión de JWT.
- **Bcrypt**: Para el hasheo de contraseñas.
- **Pydantic Settings**: Gestión de variables de entorno.

---

## 🔒 Control de Seguridad (RBAC)

El sistema permite proteger rutas de tres niveles:
1. **Autenticación**: Solo requiere token JWT válido.
2. **Roles**: Requiere pertenecer a un rol específico (ej: `["admin", "supervisor"]`).
3. **Permisos**: Requiere tener permisos granulares (ej: `["user.create", "user.edit"]`).

### Ejemplo de Configuración en Ruteo:

```python
router.add_use_case(
    path="/",
    method="POST",
    handler_instance=user_service,
    handler_method="create_user",
    schema=CreateUserSchema,
    protected=True,
    required_roles=["admin"],             # Solo permite a estos roles
    required_permissions=["user.create"]  # Debe tener estos permisos (O admin.full_access)
)
```

## 🔑 Ejemplo de JWT Payload

```json
{
  "id": 1,
  "email": "user@email.com",
  "roles": ["Administrador"],
  "permisos": ["admin.full_access"]
}
```

---

## ⚙️ Configuración e Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <repo-url>
   cd s_rbac
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de Entorno**:
   Crea un archivo `.env` en la raíz con el siguiente contenido:
   ```env
   DATABASE_URL=postgresql://user:pass@localhost/db_name
   TIMEZONE=America/Lima
   JWT_SECRET_KEY=tu_llave_secreta_super_segura
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

5. **Ejecutar la aplicación**:
   ```bash
   uvicorn main:app --reload
   ```

---

## 🛡️ BaseUseCaseHandler: El Corazón del Proyecto

El `BaseUseCaseHandler` orquestra cada petición siguiendo este flujo:
1. **Autenticación**: Verifica el JWT en los headers.
2. **Autorización**: Valida roles y permisos (incluyendo el bypass de `admin.full_access`).
3. **Validación**: Parsea y valida el cuerpo de la petición contra el schema Pydantic definido.
4. **Transacción**: Abre una sesión de base de datos (`atomic transaction`) para métodos de escritura o una sesión simple para lectura.
5. **Ejecución**: Llama al método del servicio correspondiente.
6. **Respuesta**: Captura excepciones globales y devuelve un JSON estandarizado.

---

## ▶️ Quick Demo Flow

1. Login → receive JWT
2. Use token to access protected routes
3. Roles and permissions are validated automatically
4. admin.full_access bypasses permission checks

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo y modificarlo libremente para tus proyectos personales o comerciales.
