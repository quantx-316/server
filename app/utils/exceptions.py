from fastapi import Request, HTTPException, status
from app.main import app


class AuthenticationException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


@app.exception_handler(AuthenticationException)
async def authentication_exception_handler(request: Request, exception: AuthenticationException):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        details=exception.msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


class ResourceNotFoundException(Exception):
    def __init__(self, msg: str):
        self.msg = msg 


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request: Request, exception: ResourceNotFoundException):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        details=exception.msg, 
    )


UserNotFoundException = ResourceNotFoundException("User not found")