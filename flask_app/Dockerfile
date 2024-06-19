FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Crear y activar un entorno virtual
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Copiar e instalar las dependencias del archivo requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Crear un usuario no root y cambiar a ese usuario
RUN useradd -m myuser
USER myuser

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
