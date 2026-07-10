from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.persistence.models import CbamRecordModel
from app.core.domain.models import CbamRecord
from app.core.domain.ports.record_repository import RecordRepository


class SqlAlchemyRecordRepository(RecordRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, record: CbamRecord) -> CbamRecord:
        model = CbamRecordModel(**{k: v for k, v in record.__dict__.items()})
        self._session.add(model)
        await self._session.commit()
        return record

    async def find_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[Sequence[CbamRecord], int]:
        total = await self.count()

        offset = (page - 1) * page_size
        stmt = select(CbamRecordModel).offset(offset).limit(page_size)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        records = [self._to_domain(m) for m in models]
        return records, total

    async def count(self) -> int:
        stmt = select(CbamRecordModel)
        result = await self._session.execute(stmt)
        return len(result.scalars().all())

    def _to_domain(self, model: CbamRecordModel) -> CbamRecord:
        return CbamRecord(
            eori_number=model.eori_number,
            declarant_legal_name=model.declarant_legal_name,
            declarant_address=model.declarant_address,
            contact_person=model.contact_person,
            competent_authority=model.competent_authority,
            cbam_account_number=model.cbam_account_number,
            data_owner=model.data_owner,
            taric_code=model.taric_code,
            cn_code=model.cn_code,
            goods_description=model.goods_description,
            sector_category=model.sector_category,
            product_type=model.product_type,
            import_volume=model.import_volume,
            date_of_importation=model.date_of_importation,
            country_of_origin=model.country_of_origin,
            customs_declaration_ref=model.customs_declaration_ref,
            supplier_name=model.supplier_name,
            notes_comments=model.notes_comments,
        )
