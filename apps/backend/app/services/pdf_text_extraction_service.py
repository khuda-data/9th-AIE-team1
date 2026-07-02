from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.codes import ErrorCode
from app.core.errors import BusinessError


class PdfTextExtractionService:
    def extract(self, content: bytes) -> str:
        if not content:
            raise BusinessError(ErrorCode.EMPTY_PDF)

        try:
            reader = PdfReader(BytesIO(content))
        except PdfReadError as exc:
            raise BusinessError(ErrorCode.INVALID_PDF) from exc

        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception as exc:
                raise BusinessError(ErrorCode.ENCRYPTED_PDF) from exc

        text_parts = []
        for page_number, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text() or ""
            except Exception as exc:
                raise BusinessError(ErrorCode.PDF_TEXT_EXTRACTION_FAILED, f"page {page_number}") from exc
            if page_text.strip():
                text_parts.append(page_text.strip())

        text = "\n\n".join(text_parts).strip()
        if not text:
            raise BusinessError(ErrorCode.EMPTY_PDF_TEXT)
        return text
