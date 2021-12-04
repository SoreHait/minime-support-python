class SQLQueryException(Exception):
    def __init__(self, resp = None):
        self.resp = resp

class UserNotFoundException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -5,
            'msg': 'no such user! check your card id.'
        })

class TableNotAvailableException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -5,
            'msg': 'not an available table name'
        })

class TableNameNoEntryException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -4,
            'msg': 'input table name'
        })

class CardNoEntryException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -3,
            'msg': 'input your card id! (in bin/DEVICE/felica.txt or aime.txt)'
        })

class CardInvalidException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -5,
            'msg': 'invalid card id!'
        })

class ActionInvalidException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -3,
            'msg': 'invalid action!'
        })

class ParamInsufficientException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -3,
            'msg': 'modify action should pass item id & item count!'
        })

class ItemIdInvalidException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -3,
            'msg': 'invalid item id!'
        })

class ModifyInfoNotFoundException(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -3,
            'msg': 'input modify info! (user name or team name)'
        })

class ModifyFailure(SQLQueryException):
    def __init__(self):
        super().__init__({
            'code': -6,
            'msg': 'modify error!'
        })
