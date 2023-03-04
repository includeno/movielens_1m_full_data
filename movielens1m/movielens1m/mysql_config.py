import pymysql
def create_connection():
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root123456',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_aws_connection():
    connection = pymysql.connect(host='dbs-mysql.cirpywua5kjp.ap-east-1.rds.amazonaws.com',
                            user='admin',
                            password='nacos4HBlv3==',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection