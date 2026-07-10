from app.adapters.validation.pipeline import ValidationPipeline
from app.adapters.validation.validators.allowed_values import (
    AllowedValuesValidator,
)
from app.adapters.validation.validators.cn_code import CnCodeValidator
from app.adapters.validation.validators.contact_person import (
    ContactPersonValidator,
)
from app.adapters.validation.validators.country import CountryValidator
from app.adapters.validation.validators.date_format import DateFormatValidator
from app.adapters.validation.validators.eori import EoriValidator
from app.adapters.validation.validators.length import LengthValidator
from app.adapters.validation.validators.numeric import PositiveNumericValidator
from app.adapters.validation.validators.required import RequiredValidator


REQUIRED_FIELDS = [
    "eori_number",
    "declarant_legal_name",
    "declarant_address",
    "contact_person",
    "competent_authority",
    "cbam_account_number",
    "data_owner",
    "cn_code",
    "goods_description",
    "sector_category",
    "product_type",
    "import_volume",
    "date_of_importation",
    "country_of_origin",
    "supplier_name",
]

ALLOWED_PRODUCT_TYPES = {"Simple Goods", "Complex Goods"}

CN_CODE_LENGTH = {"cn_code": (8, 8)}


def create_default_validator() -> ValidationPipeline:
    return ValidationPipeline(
        validators=[
            RequiredValidator(fields=REQUIRED_FIELDS),
            LengthValidator(fields=CN_CODE_LENGTH),
            PositiveNumericValidator(fields=["import_volume"]),
            EoriValidator(),
            CnCodeValidator(),
            ContactPersonValidator(),
            DateFormatValidator(),
            CountryValidator(),
            AllowedValuesValidator(
                fields={"product_type": ALLOWED_PRODUCT_TYPES}
            ),
        ]
    )
