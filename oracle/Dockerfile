FROM gvenzl/oracle-xe:21.3.0

# Variables de entorno por defecto
ENV ORACLE_PASSWORD=oracle
ENV APP_USER=appuser
ENV APP_USER_PASSWORD=appuserpwd
ENV APP_DB=XE

# Crear un usuario para las pruebas
COPY init.sql /container-entrypoint-initdb.d/
