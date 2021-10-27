from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from claims_solutions_api.models import company

from claims_solutions_api.schemas.company import CompanySchema
from claims_solutions_api.models.company import CompanyModel
from claims_solutions_api.messages import SuccessMessage
from claims_solutions_api.errors import (
    InternalServerError,
    CompanyAlreadyExistsError,
    CompanyNotExistsError
)

company_schema = CompanySchema()
company_schema_list = CompanySchema(many=True)

class Company(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name):
        company = CompanyModel.find_by_name(name)
        if company:
            return SuccessMessage(
                "company",
                name,
                "search",
                company_schema.dump(company)
            ).get_msg(), 200
        raise CompanyNotExistsError

    @classmethod
    @jwt_required(fresh=True)
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
        ).get_msg(), 201

    @classmethod
    @jwt_required(fresh=True)
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
        ).get_msg(), 200


class CompanyList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        print(f"user id: {user_id}")
        companies = company_schema_list.dump(CompanyModel.find_all())

        if user_id:
            data = {
                "companies": companies
            }
        else:
            company_names = []
            for company in companies:
                company_names.append(company['name'])
            data= {
                "companies": company_names
            }

        return SuccessMessage(
            "company",
            "company list",
            "list",
            data
        ).get_msg(), 200