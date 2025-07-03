# Dockerfile para o servidor MCP de previsão do tempo em Python para Easypanel

# Use uma imagem base Python oficial.
# Preferimos uma versão slim para um tamanho de imagem menor.
FROM python:3.10-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências especificadas no requirements.txt
RUN pip install uv && \
    uv pip install -r requirements.txt --system

# Copia o restante do código da aplicação para o diretório de trabalho
COPY weather.py .

# Expõe a porta que o Uvicorn estará escutando.
EXPOSE 8000

# --- ALTERAÇÃO PRINCIPAL AQUI ---
# Comando para iniciar o servidor Uvicorn.
# Agora, apontamos diretamente para 'weather:app', pois 'app' está definida
# no escopo global do weather.py como mcp.app
CMD ["uvicorn", "weather:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
