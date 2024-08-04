from io import BytesIO

import pypdf
from flask import Flask, Response, render_template, request, send_file
from pypdf import PageObject, PdfReader, PdfWriter

from .paper_size import a4_height, b5_height

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'none'; frame-ancestors 'none';"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")
    if file is None:
        return make_bad_request_response()

    scale = request.form.get("scale")
    if scale not in ["a4", "b5"]:
        return make_bad_request_response()

    try:
        reader = PdfReader(file)
    except pypdf.errors.EmptyFileError:
        return make_bad_request_response("PDF is empty")
    except pypdf.errors.PyPdfError:
        return make_bad_request_response("Failed to read uploaded PDF file")

    writer = PdfWriter()

    for page in reader.pages:
        if scale == "a4":
            scale_to_fit(page, a4_height)
        elif scale == "b5":
            scale_to_fit(page, b5_height)
        writer.add_page(page)

    writer.add_metadata(reader.metadata)

    bytes_stream = BytesIO()
    writer.write(bytes_stream)

    bytes_stream.seek(0)
    return send_file(
        bytes_stream, mimetype="application/pdf", download_name=file.filename
    )


def make_bad_request_response(message: str | None) -> Response:
    """Create a response with the given message and status code 400."""

    return Response(message, status=400, mimetype="text/plain")


def scale_to_fit(page: PageObject, size: float) -> None:
    """Scale the page to fit inside the given size, preserving aspect ratio."""

    width = page.mediabox.width
    height = page.mediabox.height

    if width > height:
        page.scale_to(size, height * size / width)
    else:
        page.scale_to(width * size / height, size)
