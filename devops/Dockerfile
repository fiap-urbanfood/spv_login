FROM python:3.12-slim

# Parametros environment
ARG USER=appuser
ENV HOME=/home/"$USER"

# Variaveis de ambiente
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Config Tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl \
      bash \
      netcat-openbsd \
      sudo \
      vim \
      less \
      net-tools \
      procps

# Instalar dependências do sistema
RUN apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Config Timezones
RUN apt-get install -y tzdata \
  && cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
  && echo "America/Sao_Paulo" > /etc/timezone \
  apt-get clean all

# Add User
RUN addgroup --gid 1000 "$USER"
RUN adduser  --gid 1000 --disabled-password --gecos '' --home "$HOME" "$USER"

# Config sudoers
RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/"$USER"
RUN chmod 0440 /etc/sudoers.d/"$USER"

# Defina o diretório do APP
USER "$USER"
WORKDIR "$HOME/app"

# Copia os arquivos do projeto
COPY --chown="$USER:$USER" --chmod=700 . $HOME/app

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip --user

# Instala as dependencias
RUN pip3 install --no-cache-dir -r requirements.txt

# Sobe o backend
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "main.py"]
CMD ["python", "criar_tabelas.py"]