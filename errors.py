from werkzeug.exceptions import HTTPException

class InternalServerError(HTTPException):
    pass

class CompanyAlreadyExistsError(HTTPException):
    pass

class CompanyNotExistsError(HTTPException):
    pass

class UnauthorizedError(HTTPException):
    pass

class UserNotConfirmedError(HTTPException):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "CompanyAlreadyExistsError": {
        "message": "Company with given name already exists",
        "status": 400
    },
    "CompanyNotExistsError": {
        "message": "Company with given id doesn't exists",
        "status": 404
    },
    "UnauthorizedError": {
        "message": "Not authorized for this request",
        "status": 401
    },
    "UserNotConfirmedError": {
        "message": "User not confirmed",
        "status": 400
    }
}