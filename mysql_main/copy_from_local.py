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

local_conn=create_connection()
remote_conn=create_aws_connection()

try:
    # 获取本地数据库游标
    local_cursor = local_conn.cursor()

    # 获取远程数据库游标
    remote_cursor = remote_conn.cursor()

    # 从本地数据库中选择所有行
    local_cursor.execute("SELECT * FROM imdb_movies_links")

    data=local_cursor.fetchall()

    # 遍历所有行并将其插入到远程数据库中
    for row in data:
        insert_query = f"INSERT INTO imdb_movies_links(name, url, completed, spider_completed, create_time, update_time) " \
                       f"VALUES ('{row['name']}', '{row['url']}', {row['completed']}, {row['spider_completed']}, '{row['create_time']}', '{row['update_time']}')"
        remote_cursor.execute(insert_query)

    # 提交事务
    remote_conn.commit()

    print("复制成功")

except Exception as e:
    # 如果发生错误，则回滚事务
    print("发生错误：", e)
    remote_conn.rollback()

finally:
    # 关闭本地和远程数据库连接
    local_conn.close()
    remote_conn.close()