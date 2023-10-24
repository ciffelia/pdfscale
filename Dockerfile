FROM python:3.12.0-slim-bookworm

RUN useradd --create-home --user-group pdfscale
USER pdfscale
WORKDIR /home/pdfscale/app

COPY requirements.lock .

RUN sed '/^-e/d' requirements.lock > requirements.txt && \
    pip install -r requirements.txt

COPY . .

RUN pip install --no-deps -e .

EXPOSE 8000

ENTRYPOINT ["python", "-m", "gunicorn", "-b", "0.0.0.0", "pdfscale:app"]
