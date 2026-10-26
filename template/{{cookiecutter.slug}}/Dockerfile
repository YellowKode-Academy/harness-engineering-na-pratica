FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd --create-home agente && chown -R agente /app
USER agente

ENV AGENTE_AMBIENTE=producao
CMD ["python", "-m", "{{ cookiecutter.__pacote }}"]
