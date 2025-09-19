# POC PL/SQL CI/CD

## 📝 Resumen del Proyecto

Este proyecto es una **Prueba de Concepto (POC)** que implementa un entorno de **CI/CD para scripts de base de datos PL/SQL** utilizando GitLab y Oracle Database. El objetivo principal es demostrar cómo automatizar el despliegue, versionado y testing de código PL/SQL en un ambiente controlado.

## 🏗️ Arquitectura

El proyecto está compuesto por tres servicios principales orquestados con Docker Compose:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitLab CE     │    │  GitLab Runner  │    │  Oracle XE 21c  │
│   (Puerto 8080) │────│                 │────│  (Puerto 1521)  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes:

1. **Oracle Database XE 21c**: Base de datos con usuario `appuser` preconfigurado
2. **GitLab Community Edition**: Servidor Git con pipelines CI/CD integrados
3. **GitLab Runner**: Ejecutor de pipelines para automatizar despliegues

## 🚀 Características

- ✅ **Entorno containerizado** completo con Docker
- ✅ **Base de datos Oracle XE** preconfigurada con usuario de aplicación
- ✅ **GitLab integrado** para control de versiones y CI/CD
- ✅ **Script de consolidación** para generar deploys unificados
- ✅ **Generación automática de backups** de objetos PL/SQL
- ✅ **Configuración de volúmenes persistentes** para datos

## 📂 Estructura del Proyecto

```
poc-plsql-ci/
├── docker-compose.yml          # Orquestación de servicios
├── deploy.py                   # Script de consolidación de deploys
├── gitlab/
│   └── Dockerfile             # Imagen customizada de GitLab
├── oracle/
│   ├── Dockerfile             # Imagen customizada de Oracle
│   └── init.sql              # Script de inicialización DB
└── scripts/
    └── generar_backup.sql     # Script para backup de objetos PL/SQL
```

## 🛠️ Requisitos

- **Docker** (v20.10 o superior)
- **Docker Compose** (v3.9 o superior)
- **Python 3.x** (para el script de deploy)
- Al menos **8GB de RAM** (recomendado para Oracle + GitLab)
- **20GB de espacio en disco** libre

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd poc-plsql-ci
```

### 2. Levantar los servicios

```bash
# Construir y levantar todos los servicios
docker-compose up -d

# Verificar que los servicios estén ejecutándose
docker-compose ps
```

### 3. Acceder a los servicios

Una vez levantados los contenedores:

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **GitLab** | http://localhost:8080 | Usuario: `root` / Password: Ver logs de GitLab |
| **Oracle DB** | localhost:1521 | Usuario: `appuser` / Password: `appuserpwd` |

### 4. Configurar GitLab (Primera vez)

```bash
# Obtener la contraseña inicial de GitLab
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

### 5. Registrar GitLab Runner

```bash
# Obtener el token de registro desde GitLab UI (Admin Area → Runners)
docker exec -it gitlab-runner gitlab-runner register \
  --url http://gitlab.local \
  --registration-token <TOKEN> \
  --executor docker \
  --docker-image docker:latest
```

## 💾 Conexión a Oracle Database

### Credenciales por defecto:

- **Host**: localhost
- **Puerto**: 1521
- **SID**: XE
- **Usuario**: appuser
- **Contraseña**: appuserpwd

### Ejemplo de conexión con SQLcl:

```bash
sql appuser/appuserpwd@localhost:1521/XE
```

## 📋 Uso del Proyecto

### 1. Generar Backup de Objetos PL/SQL

```bash
# Ejecutar script de backup (requiere SQLcl o SQL*Plus)
sqlcl appuser/appuserpwd@localhost:1521/XE @scripts/generar_backup.sql [nombre_backup]
```

Este comando genera un archivo `backup_[nombre].sql` en la carpeta `backups/` con todos los objetos PL/SQL (procedimientos, funciones, packages, triggers) del esquema `APPUSER`.

### 2. Consolidar Scripts de Deploy

```bash
# Ejecutar el script Python para consolidar todos los .sql
python deploy.py
```

Este script:
- Recorre la carpeta `scripts/`
- Consolida todos los archivos `.sql` en orden alfabético
- Genera un archivo `deploy_YYYYMMDD_HHMMSS.sql` con timestamp
- Añade separadores `/` entre scripts para Oracle

### 3. Pipeline CI/CD

El proyecto está preparado para implementar pipelines GitLab que pueden:
- Validar sintaxis PL/SQL
- Ejecutar tests automatizados
- Desplegar cambios a diferentes ambientes
- Generar backups automáticos

## 🔧 Comandos Útiles

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Reiniciar un servicio específico
docker-compose restart oracle

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes (⚠️ CUIDADO: elimina datos)
docker-compose down -v

# Acceder al contenedor de Oracle
docker exec -it oracle-xe bash

# Acceder al contenedor de GitLab
docker exec -it gitlab bash
```

## 🔍 Solución de Problemas

### Oracle no inicia correctamente
```bash
# Verificar logs de Oracle
docker logs oracle-xe

# Verificar que el puerto no esté en uso
netstat -an | findstr 1521
```

### GitLab no responde
```bash
# Verificar estado de GitLab
docker exec -it gitlab gitlab-ctl status

# Restart de GitLab
docker exec -it gitlab gitlab-ctl restart
```

### Problemas de memoria
```bash
# Verificar uso de recursos
docker stats

# Aumentar memoria disponible para Docker Desktop
# Settings → Resources → Memory (mínimo 8GB)
```

## 📚 Recursos Adicionales

- [Documentación Oracle XE](https://docs.oracle.com/en/database/oracle/oracle-database/21/xeinl/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es una POC con fines educativos y de demostración.

---

**Nota**: Este es un ambiente de desarrollo/testing. Para producción, considera implementar medidas adicionales de seguridad, backup y monitoreo.