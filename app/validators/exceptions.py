class DatabaseQueryException(Exception):
    pass

class EventDoNotExist(Exception):
    " Raised when there is no event we looking for. "

class UserDoestNotExist(Exception):
    " Raised when there is no user we looking for. "

class InvalidUserType(Exception):
    " Raised when user is wrong type. "

class InvalidParticipantRole(Exception):
    " Raised when user is ment to be written to database with invalid participant role"

