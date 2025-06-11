# Dockerfile para o servidor MCP de previsão do tempo em Python para Easypanel

# Use uma imagem base Python oficial.
# Preferimos uma versão slim para um tamanho de imagem menor.
FROM python:3.10-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências especificadas no requirements.txt
# Adicionamos '--system' para que 'uv' instale as dependências no ambiente global do container.
RUN pip install uv && \
    uv pip install -r requirements.txt --system

# Copia o restante do código da aplicação para o diretório de trabalho
COPY weather.py .

# Expõe a porta que o Uvicorn estará escutando.
# Esta é a porta 8000 que definimos no weather.py.
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn quando o container for executado.
# 'uvicorn' executa a aplicação ASGI definida em 'weather:app'.
# 'weather' se refere ao arquivo weather.py e 'app' à variável 'app' nele.
# --host 0.0.0.0 para escutar em todas as interfaces.
# --port 8000 para escutar na porta 8000.
# --workers 1 (ou mais, dependendo da sua necessidade) para um ambiente de produção.
# --log-level info para ver logs úteis.
CMD ["uvicorn", "weather:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
