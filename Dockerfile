FROM python:3.12.0-slim-bookworm

RUN useradd --create-home --user-group pdfscale
USER pdfscale
WORKDIR /home/pdfscale/app

COPY requirements.lock .

RUN sed -i '/^-e/d' requirements.lock && \
    PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY . .

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir --no-deps -e .

EXPOSE 8000

ENTRYPOINT ["python", "-m", "gunicorn", "-b", "0.0.0.0", "pdfscale:app"]
