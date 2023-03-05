import pymysql
def create_connection():
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root123456',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection
connection=create_connection()
cursor = connection.cursor()

# 查询表中的重复数据
query = ("SELECT name, url, COUNT(name) as count "
         "FROM imdb_movies_links "
         "GROUP BY name, url "
         "HAVING count > 1")
cursor.execute(query)
li=cursor.fetchall()
#print(li)

# 遍历查询结果，并删除重复行
for item in li:
    column1=item['name']
    column2=item['url']
    # 查询重复行
    query = ("SELECT id FROM imdb_movies_links "
             "WHERE name = %s AND url = %s "
             "ORDER BY id DESC")
    cursor.execute(query, (column1, column2))
    ids=cursor.fetchall()
    print(ids)
    row_ids = [row['id'] for row in ids]
    print(row_ids)
    # 删除重复行
    for row_id in row_ids[1:]:
        query = "DELETE FROM imdb_movies_links WHERE id = %s"
        cursor.execute(query, (row_id,))
        connection.commit()

# 关闭MySQL连接
cursor.close()
connection.close()
