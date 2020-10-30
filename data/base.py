class BadRequestForQuery(Exception):
    def __init__(self, table, necessary_args):
        message = f'Error: to make a query for {table} table, you must pass at least one of these parameters: {necessary_args}.'
        super().__init__(message)

class RowAlreadyExists(Exception):
    def __init__(self, table):
        self.__message = f'Error: already exists a row in {table} table with at least one unique column with the same value.'

        super().__init__(self.__message)

class BasePackage():
    session = None

    def __init__(self, session_scope):
        self.session_scope = session_scope

    def insert_object(self, table, **kwargs):
        """
        This function inserts an object in the given table.

        Args:
            table: A sqlalchemy table.
            **kwargs: A dict with all the columns necessary to insert a row in the above table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            obj, None: Otherwise, with 'obj' being the row inserted in the table.
        """
        try:
            with self.session_scope() as session:
                obj = table(**kwargs)
                session.add(obj)
                session.commit()

            return obj, None
        except Exception as err:
            print(f'Error: {err}')

            return None, err

    def get_objects_by_attr(self, table, attr, values=[]):
        """
        This function gets all the objects whose attr is in values list.

        Args:
            table: A sqlalchemy table.
            attr: An attribute of above sqlalchemy table.
            values: A list with the required values for attr.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        if values:
            try:
                with self.session_scope() as session:
                    objects = session.query(table).filter(attr.in_(values)).all()

                return objects, None
            except Exception as err:
                print(f'Error: {err}')

                return None, err
        else:
            return [], None