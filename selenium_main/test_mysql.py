import pymysql

def create_connection():
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root123456',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

connection=create_connection()
cursor=connection.cursor()

def get_keywords(count):
    if(count==None):
        count=10
    # 查询语句
    sql = f"SELECT id, name, url FROM imdb_movies_links WHERE completed=0 LIMIT {count}"

    # 执行查询
    cursor.execute(sql)
    results = cursor.fetchall()
    result_list=[]
    for result in results:
        result_list.append(result["name"])
    return result_list

def get_urls(count):
    if(count==None):
        count=10
    # 查询语句
    sql = f"SELECT id, name, url FROM imdb_movies_links WHERE completed=0 LIMIT {count}"

    # 执行查询
    cursor.execute(sql)
    results = cursor.fetchall()
    result_list=[]
    for result in results:
        result_list.append(result["url"])
    return result_list

keywords=get_keywords(10)
print(keywords)
connection.close()
