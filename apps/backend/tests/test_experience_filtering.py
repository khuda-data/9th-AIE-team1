from app.repositories.experience_repository import ExperienceRepository
from app.schemas.document import TextDocumentCreateRequest
from app.schemas.llm import ExperienceDraft, ExperienceExtractionResult
from app.services.document_processing_service import DocumentProcessingService
from app.services.document_service import DocumentService


class EmptyTitleOnlyExtractor:
    def extract(self, cleaned_text: str) -> ExperienceExtractionResult:
        return ExperienceExtractionResult(experiences=[ExperienceDraft(title="경험1")])


def test_document_processing_drops_title_only_experience_drafts(db_session):
    user_id = "00000000-0000-0000-0000-000000000004"
    document = DocumentService(db_session).create_text_document(
        TextDocumentCreateRequest(
            user_id=user_id,
            source_type="notion",
            title="Notion root",
            text="## 경험1",
        )
    )

    status, experience_count, question_count = DocumentProcessingService(
        db_session,
        extractor=EmptyTitleOnlyExtractor(),
    ).process(document.id)

    assert status == "processed"
    assert experience_count == 0
    assert question_count == 0
    assert ExperienceRepository(db_session).list_by_document(document.id) == []
