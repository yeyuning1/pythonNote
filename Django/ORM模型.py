from pymysql import connect

DATABASES = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD': 'mysql',
    'NAME': 'django_demo'
}


class Filed(object):
    def __init__(self, filed_type):
        self.filed_type = filed_type


class CreateClass(type):
    def __new__(cls, class_name, super_name, attrs):
        create_params = {}
        for key, value in attrs.items():
            if isinstance(value, Filed):
                create_params[key] = value.filed_type
        attrs['create_params'] = create_params
        attrs['table_name'] = class_name.lower()

        return type.__new__(cls, class_name, super_name, attrs)


class DBOperation(object, metaclass=CreateClass):
    @staticmethod
    def connect():
        conn = connect(host=DATABASES['HOST'],
                       port=DATABASES['PORT'],
                       user=['USER'],
                       password=DATABASES['PASSWORD'],
                       database=DATABASES['NAME'])
        return conn

    def create(self):
        with self.connect() as conn:
            with conn.cursor() as cs:
                sql_string = """create table if not exists %s (%s) charset=utf8;"""
                table = self.table_name
                fields = list()
                for key, value in self.create_params.items():
                    fields.append("%s %s", (key, value))

                cs.execute(sql_string, (table, ','.join(fields)))

    def insert(self, **kwargs):
        with self.connect() as conn:
            with conn.cursor() as cs:
                sql_string = """insert into %s(%s) values ('%s');"""
                table = self.table_name
                fields = []
                values = []
                for key, value in kwargs.items():
                    fields.append(key)
                    values.append(value)
                cs.execute(sql_string, (table, fields, values))

    def update(self, where='1=1', **kwargs):
        with self.connect() as conn:
            with conn.cursor() as cs:
                sql_string = """update %s set %s where %s;"""
                items = list()
                for key, value in kwargs.items():
                    items.append(str(key) + '=' + str(value))
                cs.execute(sql_string, (self.table_name, ','.join(items), where))

    def delete(self, **kwargs):
        with self.connect() as conn:
            with conn.cursor() as cs:
                sql_string = """delete from %s where %s;"""
                items = list()
                for key, value in kwargs.items():
                    items.append(str(key) + '=' + str(value))
                cs.execute(sql_string, (self.table_name, ','.join(items)))


