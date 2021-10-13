from flask_restful import Resource
from flask import request

from schemas.company import CompanySchema
from models.company import CompanyModel
from resources.messages import SuccessMessage
from errors import (
    InternalServerError,
    CompanyAlreadyExistsError,
    CompanyNotExistsError
)

company_schema = CompanySchema()
company_schema_list = CompanySchema(many=True)

class Company(Resource):
    @classmethod    
    def get(cls, name):
        company = CompanyModel.find_by_name(name)
        if company:
            return SuccessMessage(
                "company",
                name,
                "insert",
                company_schema.dump(company)
            ).__dict__, 200
        raise CompanyNotExistsError

    @classmethod    
    def post(cls, name: str):
        if CompanyModel.find_by_name(name):
            return CompanyAlreadyExistsError

        company_json = request.get_json()
        company_json["name"] = name

        #
        # "CompanyModel" is a subclass of "db.Model" which accepts keyword args.
        #
        company = company_schema.load(company_json)

        try:
            company.save_to_db()
        except:
            raise InternalServerError

        return SuccessMessage(
            "company",
            name,
            "insert",
            company_schema.dump(company)
        ).__dict__, 201

    @classmethod    
    def delete(cls, name: str):
        company = CompanyModel.find_by_name(name)
        if company:
            try:
                company.delete_from_db()
            except:
                raise InternalServerError

        return SuccessMessage(
            "company",
            name,
            "insert",
            company_schema.dump(company)
        ).__dict__, 200


class CompanyList(Resource):
    @classmethod    
    def get(cls):
        return SuccessMessage(
            "company",
            "company list",
            "list",
            {"companies": company_schema_list.dump(CompanyModel.find_all())}
        ).__dict__, 200