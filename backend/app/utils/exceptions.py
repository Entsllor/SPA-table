from fastapi import HTTPException, status


class BaseAppException(Exception):
    as_http: HTTPException


class IncorrectLoginOrPassword(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


class CredentialsException(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


class InactiveUser(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Current user is inactive",
        headers={"WWW-Authenticate": "Bearer"},
    )


class UserNotFoundError(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to find this User",
        headers={"WWW-Authenticate": "Bearer"},
    )


class Forbidden(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Sorry, but you do not have enough rights",
        headers={"WWW-Authenticate": "Bearer"},
    )


class ExpectedOneInstance(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="There are duplicates that cannot be processed"
    )


class InstanceNotFound(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Failed to find this object"
    )


class ExpectedUniqueEmail(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This email is already taken"
    )


class ExpectedUniqueUsername(BaseAppException):
    as_http = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This username is already taken"
    )
