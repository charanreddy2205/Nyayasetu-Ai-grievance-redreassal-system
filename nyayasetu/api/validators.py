from typing import Any
import uuid
import mimetypes
from pathlib import Path
from django.core.exceptions import ValidationError
from PIL import Image as PILImage

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_and_sanitize_upload(uploaded_file) -> Any:
    """
    Validates file size, whitelist extension, content MIME type,
    and checks image structure integrity. Sanitize filename using random UUID.
    """
    if not uploaded_file:
        return None
        
    # 1. Size constraint
    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValidationError("File size exceeds 5MB limit.")
        
    # 2. Extension validation
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Only JPG, JPEG, PNG, and GIF images are allowed.")
        
    # 3. Path traversal protection: sanitize name
    filename_only = Path(uploaded_file.name).name
    
    # 4. MIME type check
    mime_type, _ = mimetypes.guess_type(filename_only)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValidationError("Invalid file content type.")
        
    if uploaded_file.content_type not in ALLOWED_MIME_TYPES:
        raise ValidationError("Invalid uploaded MIME type headers.")
        
    # 5. Image integrity validation (Pillow verification)
    try:
        img = PILImage.open(uploaded_file)
        img.verify()
        uploaded_file.seek(0)  # Reset pointer for saving
    except Exception:
        raise ValidationError("Uploaded file is not a valid or secure image.")
        
    # 6. Sanitize filename using randomized UUID to block remote execution / path traversal
    uploaded_file.name = f"{uuid.uuid4().hex}{ext}"
    return uploaded_file
