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
    uv pip install -r requirements.txt --system && \
    echo "Dependencies installed v1.0.0" # Alterar este número a cada tentativa de forçar rebuild

# Copia o restante do código da aplicação para o diretório de trabalho
COPY weather.py .

# Expõe a porta que o Uvicorn estará escutando.
EXPOSE 8000

# --- ALTERAÇÃO FINAL AQUI NO CMD ---
# Comando para iniciar o servidor Uvicorn.
# Agora, 'weather:app' aponta para a variável 'app' no weather.py,
# que definimos como a instância 'mcp'.
# ... (partes anteriores) ...
CMD ["uvicorn", "weather:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
