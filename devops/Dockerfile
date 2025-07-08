FROM python:3.12-slim

# Parametros environment
ARG USER=appuser
ENV HOME=/home/"$USER"

# Variaveis de ambiente
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Config Tools
RUN apt-get update && apt-get --no-install-recommends install -y \ 
    bash \
    curl \
    less \
    netcat-openbsd \
    net-tools \
    procps \
    sudo \
    vim \
    && apt-get clean

# Instalar dependências do sistema
RUN apt-get --no-install-recommends install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && apt-get clean

# Config Timezones
RUN apt-get --no-install-recommends install -y tzdata \
  && cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
  && echo "America/Sao_Paulo" > /etc/timezone \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

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
COPY --chown="$USER:$USER" --chmod=750 ./api $HOME/app/api
COPY --chown="$USER:$USER" --chmod=644 ./core $HOME/app/core
COPY --chown="$USER:$USER" --chmod=644 ./models $HOME/app/models
COPY --chown="$USER:$USER" --chmod=644 ./schemas $HOME/app/schemas

COPY --chown="$USER:$USER" --chmod=640 ./popular_usuarios.py $HOME/app
COPY --chown="$USER:$USER" --chmod=640 ./criar_tabelas.py $HOME/app
COPY --chown="$USER:$USER" --chmod=640 ./main.py $HOME/app
COPY --chown="$USER:$USER" --chmod=640 ./requirements.txt $HOME/app

#RUN ls --recursive $HOME/app/

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip --user

# Instala as dependencias
RUN pip3 install --no-cache-dir -r requirements.txt

# Sobe o backend
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "main.py"]
CMD ["python", "criar_tabelas.py"]