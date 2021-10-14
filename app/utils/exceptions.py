from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.main import app


class AuthenticationException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


@app.exception_handler(AuthenticationException)
async def authentication_exception_handler(request: Request, exception: AuthenticationException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exception.msg},
        headers={"WWW-Authenticate": "Bearer"},
    )


class ResourceNotFoundException(Exception):
    def __init__(self, msg: str):
        self.msg = msg 


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request: Request, exception: ResourceNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, 
        content={"message": exception.msg},
    )


UserNotFoundException = ResourceNotFoundException("User not found")
AlgoNotFoundException =  ResourceNotFoundException("Algo not found")

class BadRequestException(Exception):
    def __init__(self, msg: str):
        self.msg = msg 


@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exception: BadRequestException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, 
        content={"message": exception.msg},
    )


UpdateException = BadRequestException("Update failed")
CreateException = BadRequestException("Create failed")


class AccessDeniedException(Exception):
    def __init__(self, msg: str):
        self.msg = msg 


@app.exception_handler(AccessDeniedException)
async def access_denied_exception_handler(request: Request, exception: AccessDeniedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        CONTENT={"message": exception.msg}
    )


NotOwnerException = AccessDeniedException("User is not the owner of requested resource")
