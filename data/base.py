class BasePackage():
    session = None

    def __init__(self, session_scope):
        self.session_scope = session_scope