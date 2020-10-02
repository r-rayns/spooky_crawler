class Dictionary():
    def __init__(self, value):
        self.value = value
        self.error = None

    # safely retrieve value from dictonary else set value to None
    def safeGet(self, *keys):
        for index, key in enumerate(keys):
            try:
                self.value = self.value[key]
            except KeyError:
                if(index == len(keys) - 1):
                    # no key worked, error
                    self.error = KeyError
                    self.value = None
                    return self
        return self

    # sets value to the result of a function if
    # original value could not be retrieved from the dictonary
    def onError(self, fn):
        if self.error:
            self.value = fn()
        return self


class Database():
    import psycopg2
    from configparser import ConfigParser

    logger = None

    def __init__(self, logger):
        self.logger = logger

    def connect(self, filename='database.ini', section='postgresql'):
        conn = None
        try:
            config = self._getConfig(filename, section)
            self.logger.info('Connecting to the PostgreSQL database...')
            conn = self.psycopg2.connect(**config)
            return conn

        except (Exception, self.psycopg2.DatabaseError) as error:
            self.logger.critical(
                'Could not connect to PostgreSQL database, error: {}'.format(error))
            self.closeConnection(conn)

    def closeConnection(self, conn):
        if conn is None:
            return
        conn.close()
        self.logger.info('Database connection closed')

    def _getConfig(self, filename, section):
        parser = self.ConfigParser()
        parser.read(filename)

        dbConfig = {}
        if parser.has_section(section):
            values = parser.items(section)
            dbConfig = self._extractSectionValues(values)
        else:
            raise Exception('Section named {0} was not found in the file named {1}'
                            .format(section, filename))
        return dbConfig

    def _extractSectionValues(self, values):
        extract = {}
        for value in values:
            extract[value[0]] = value[1]
        return extract
