

class InternalServerError(Exception):
    pass

class CompanyAlreadyExistsError(Exception):
    pass

class CompanyNotExistsError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "CompanyAlreadyExistsError": {
         "message": "Company with given name already exists",
         "status": 400
     },
     "CompanyNotExistsError": {
         "message": "Company with given id doesn't exists",
         "status": 404
     }
}