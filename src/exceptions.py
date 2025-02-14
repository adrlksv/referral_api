from fastapi import HTTPException, status


class ReferralException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(ReferralException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"

class IncorrectEmailOrPasswordException(ReferralException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"

class TokenExpiredException(ReferralException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "The token has expired"

class TokenAbsentException(ReferralException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "The token is missing"

class IncorrectTokenFormatException(ReferralException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"

class UserIsNotPresentException(ReferralException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""

class GitHubAuthException(ReferralException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "GitHub authorization error"

class GitHubProfileError(ReferralException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Github profile retrieval error"

class AuthCodeException(ReferralException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Authorization code not provided"
