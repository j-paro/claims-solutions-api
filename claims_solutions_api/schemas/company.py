from claims_solutions_api.schemas import ma
from claims_solutions_api.models.company import CompanyModel


class CompanySchema(ma.SQLAlchemyAutoSchema):
    #
    # The following tells Marshmallow that the Company ID will not be specified
    # when getting a company entry.
    #
    class Meta:
        model = CompanyModel
        dump_only = ("id",)
        load_instance = True