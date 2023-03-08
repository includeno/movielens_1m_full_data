from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# 创建Chrome浏览器实例
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-software-rasterizer')


def get_keywords(count):
    if(count==None):
        count=10
    # 查询语句
    sql = f"SELECT id, name,full_name, url FROM imdb_movies_links_full WHERE completed=0 LIMIT {count}"

    # 执行查询
    cursor.execute(sql)
    results = cursor.fetchall()
    result_list=[]
    for result in results:
        result_list.append(result["full_name"])
    return result_list

def search(driver,keyword):
    # 在搜索框中输入关键词并提交搜索
    search_box = driver.find_element(By.CLASS_NAME,"imdb-header-search__input")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    # 等待搜索结果页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item")))

    # 获取搜索结果中第一个电影的链接
    first_result = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
    print(first_result)
    print(len(first_result))
    if(len(first_result)>0):
        links=first_result[0].find_elements(By.TAG_NAME,'a')
        if(len(links)>0):
            link=links[0]
            movie_url = link.get_attribute("href")
            print("movie:",keyword, movie_url)
            # 更新语句
            sql = "UPDATE imdb_movies_links_full SET url=%s, completed=1 WHERE full_name=%s"

            # 执行更新
            data = [(movie_url, keyword)]
            cursor.executemany(sql, data)
            connection.commit()

driver = webdriver.Chrome(options=options)
# 打开IMDB网站
driver.get("https://www.imdb.com/")

for tune in range(150):
    for keyword in get_keywords(10):
        search(driver=driver,keyword=keyword)
# 关闭浏览器
driver.quit()
connection.close()
