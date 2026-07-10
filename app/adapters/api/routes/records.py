from fastapi import APIRouter, Depends, Query

from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.record import RecordResponse


def create_records_router(repository_factory=None) -> APIRouter:
    router = APIRouter(tags=["Records"])

    @router.get(
        "/records",
        summary="Listar registros CBAM",
        description=(
            "Retorna una lista paginada de registros CBAM almacenados. "
            "Los resultados se ordenan por orden de inserción. "
            "Usa los parámetros page y page_size para navegar entre páginas."
        ),
        response_model=PaginatedResponse,
    )
    async def list_records(
        page: int = Query(
            1,
            ge=1,
            description="Número de página a recuperar (empieza en 1)",
        ),
        page_size: int = Query(
            20,
            ge=1,
            le=100,
            description="Cantidad de registros por página (máximo 100)",
        ),
        repo: SqlAlchemyRecordRepository = (
            Depends(repository_factory) if repository_factory else None
        ),
    ):
        records, total = await repo.find_all(
            page=page, page_size=page_size
        )
        items = [
            RecordResponse(
                eori_number=r.eori_number,
                declarant_legal_name=r.declarant_legal_name,
                declarant_address=r.declarant_address,
                contact_person=r.contact_person,
                competent_authority=r.competent_authority,
                cbam_account_number=r.cbam_account_number,
                data_owner=r.data_owner,
                taric_code=r.taric_code,
                cn_code=r.cn_code,
                goods_description=r.goods_description,
                sector_category=r.sector_category,
                product_type=r.product_type,
                import_volume=r.import_volume,
                date_of_importation=r.date_of_importation,
                country_of_origin=r.country_of_origin,
                customs_declaration_ref=r.customs_declaration_ref,
                supplier_name=r.supplier_name,
                notes_comments=r.notes_comments,
            )
            for r in records
        ]
        return PaginatedResponse(
            page=page, page_size=page_size, total=total, items=items
        )

    return router
