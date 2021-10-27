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

class ExpiredTokenError(HTTPException):
    pass

class InvalidTokenError(HTTPException):
    pass

class MisssingTokenError(HTTPException):
    pass

class RevokedTokenError(HTTPException):
    pass

class StaleTokenError(HTTPException):
    pass

class UserNotFoundError(HTTPException):
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
    },
    "ExpiredTokenError": {
        "message": "Access token has expired",
        "status": 401
    },
    "InvalidTokenError": {
        "message": "Signature verification failed",
        "status": 401
    },
    "MisssingTokenError": {
        "message": "Missing access token",
        "status": 401
    },
    "StaleTokenError": {
        "message": "You need a fresh access token",
        "status": 401
    },
    "RevokedTokenError": {
        "message": "That access token has been revoked",
        "status": 401
    },
    "UserNotFoundError": {
        "message": "User not found",
        "status": 401
    }
}