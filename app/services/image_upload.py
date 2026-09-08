"""
Author: H A (i-xul)
Repository: https://github.com/i-xul/flask-band-website-cms
File: app/services/image_upload.py
Created: 2026-08-23
Version: 0.5.0

Purpose:
    Validate, process, and store image uploads used by the band website CMS.

Overview:
    Uploaded images are decoded with Pillow rather than trusted by filename
    extension alone. Valid images are normalized, resized when necessary,
    converted to WebP, and stored under the application's static upload
    directory using randomly generated filenames.
"""

from pathlib import Path
from uuid import uuid4

from flask import current_app
from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage

# -----------------------------------------------------------------------------
# Exceptions
# -----------------------------------------------------------------------------


class ImageUploadError(Exception):
    """Raised when an uploaded image cannot be safely processed."""


# -----------------------------------------------------------------------------
# Image upload helpers
# -----------------------------------------------------------------------------


def save_image_upload(
    uploaded_file: FileStorage,
    category: str,
) -> str:
    """Validate, normalize, and save an uploaded image as WebP.

    Args:
        uploaded_file: Uploaded image received from a Flask form.
        category: Upload category, such as ``merch``, ``media``, ``shows``,
            ``band``, or ``releases``.

    Returns:
        Static-relative path suitable for storing in an ``image_path`` field.

    Raises:
        ImageUploadError: If the upload is missing, invalid, or unsupported.
    """
    if not uploaded_file or not uploaded_file.filename:
        raise ImageUploadError("No image file was selected.")

    allowed_categories = {
        "merch",
        "media",
        "shows",
        "band",
        "releases",
    }

    if category not in allowed_categories:
        raise ImageUploadError("Invalid image upload category.")

    try:
        image = Image.open(uploaded_file.stream)
        image.verify()

        uploaded_file.stream.seek(0)
        image = Image.open(uploaded_file.stream)

    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ImageUploadError("The selected file is not a valid image.") from exc

    allowed_formats = {"JPEG", "PNG", "WEBP"}

    if image.format not in allowed_formats:
        image.close()
        raise ImageUploadError("Unsupported image format. Use JPEG, PNG, or WebP.")

    max_width = current_app.config["IMAGE_UPLOAD_MAX_WIDTH"]
    max_height = current_app.config["IMAGE_UPLOAD_MAX_HEIGHT"]
    webp_quality = current_app.config["IMAGE_UPLOAD_WEBP_QUALITY"]

    image.thumbnail(
        (max_width, max_height),
        Image.Resampling.LANCZOS,
    )

    if image.mode not in {"RGB", "RGBA"}:
        image = image.convert("RGBA" if "transparency" in image.info else "RGB")

    relative_directory = Path("uploads") / category

    upload_directory = Path(current_app.static_folder) / relative_directory

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = f"{uuid4().hex}.webp"
    destination = upload_directory / filename

    try:
        image.save(
            destination,
            format="WEBP",
            quality=webp_quality,
            method=6,
        )
    except OSError as exc:
        raise ImageUploadError("The image could not be saved.") from exc
    finally:
        image.close()

    return (relative_directory / filename).as_posix()
