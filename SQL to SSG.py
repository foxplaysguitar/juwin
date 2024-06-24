import pymysql
import datetime as dt
import requests as rq
import re
import os
from PIL import Image
from pprint import pprint
from bs4 import BeautifulSoup as bs


# 資料庫連接配置
db_config = {
    'host': "192.168.0.130",
    'user': "super_admin",
    'password': "Apy^6MjqK4)De^4~*u%C",
    'database': 'locoy_article_currency',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.SSDictCursor
}

db_arr = []
db_cf = []
db_cf_full = []
db_post_title = []
db_source_page = []
db_source_site = []
db_tag = []
db_html_tag = set()

try:
    # 建立連接
    connection = pymysql.connect(**db_config)

    # 創建 cursor 物件
    with connection.cursor() as cursor:
        # 定義 SQL 查詢語句
        # sql = "SELECT * FROM unified_article_pool LIMIT 100"
        # sql = "SELECT * FROM unified_article_pool_en LIMIT 10"
        sql = "SELECT * FROM unified_article_pool_tran_ch LIMIT 1"

        # 執行 SQL 查詢
        cursor.execute(sql)

        # 獲取查詢結果
        result = cursor.fetchall()

        # 處理查詢結果
        for row in result:
            
            ssg_check = []                                              #確認內容有無重複，避免 p 裡面又有 p 的Bug
            ssg_final = []                                              #轉化為MarkDown的內容

            #Formatter 處理
            ssg_formatter = {                                          #標題、描述、首圖...等等
                'title' : row['post_title'],
                'description' : row['post_excerpt'],
                'slug' : f'article_{row['article_id']}',
                'category':['TEST-Tag'],
                'tags':['TEST-Tag'],
                'image': {'src': f'media/content-{row["article_id"]}-cover.webp',
                          'alt': f'{row["article_id"]}-cover'
                          },
                'createdAt' : str(dt.date.today()),
            }

            #處理首圖 - 1.下載首圖
            image_path = row['thumbnail']
            if not image_path :
                ssg_formatter['image']['src'] = f'media/default-cover.webp'       #如果沒提供首圖，就用預設的
            else :
                image_domain = re.findall(r'(https?://.*?)\/.*',row['source_page'])[0]
                file_name = f'content-{row["article_id"]}-cover.webp'
                image_url = image_domain + image_path
                img_res = rq.get(image_url, stream = True)
                
                if img_res.status == 200 :
                    with open(file_name, 'wb') as file :
                        for chunk in img_res.iter_content(chunk_size = 8192):
                            file.write(chunk)
                    print(f'Cover Image {file_name} Download Successful')

                    #處理首圖 - 2. 壓縮首圖
                    while os.path.getsize(f'{file_name}') // 1024 > 100 :
                        print(f'Original Size : {os.path.getsize('test.webp') // 1024}')
                        img = Image.open(f'{file_name}')
                        img.save(f'{file_name}','WEBP', quality = 90)
                        print('Compressed Complete !')
                        print(f'Current Size : {os.path.getsize('test.webp') // 1024}')

                    #處理首圖 - 3. 上傳資料庫

                    #處理首圖 - 4. 刪除本地端檔案
                    os.remove(f'{file_name}')

                else :
                    print('Cover Image Fetch Failed')
                    ssg_formatter['image']['src'] = f'media/default-cover.webp'

            #formatter 放入 ssg_final 中
            ssg_final.append('\n'.join(['---',
                f'title: {ssg_formatter['title']}',
                f'description: {ssg_formatter['description']}',
                f'slug: {ssg_formatter['slug']}',
                f'category:', 
                f'{'\n'.join(map(lambda x : f'  -  {x}',ssg_formatter['category']))}',
                f'tags',
                f'{'\n'.join(map(lambda x : f'  -  {x}',ssg_formatter['tags']))}',
                f'image:',
                f'  src: {ssg_formatter['image']['src']}',
                f'  alt: {ssg_formatter['image']['alt']}',
                f'createdAt: {ssg_formatter['createdAt']}',
                f'draft: false',
                f'updatedAt: {ssg_formatter['createdAt']}',
                f'order: 0',
                '---'])
            )

            #文章內容抓取
            post_content = row['post_content']                          #抓取資料庫的「文章內容」
            content_doc = bs(post_content, 'html.parser')               
            nodes = content_doc.select('*')                             #選取所有標籤，準備進行內容處理
            
            if not content_doc.select('h1') :
                ssg_final.append(f'# {ssg_formatter['title']}')

            for node in nodes :
                if node.text not in ssg_check :
                    if node.name == 'h1': ssg_content = f'#  {node.text}'
                    elif node.name == 'h2': ssg_content = f'##  {node.text}'
                    elif node.name == 'h3' : ssg_content = f'###  {node.text}'
                    elif node.name == 'h4' : ssg_content = f'####  {node.text}'
                    elif node.name == 'p' : ssg_content = f'{node.text}'
                    elif node.name == 'table' :
                        metas = node.select('meta')
                        for meta in metas :
                            meta.decompose()
                        ssg_content = f'{node.prettify()}'
                    elif node.name == 'ul' :
                        lists = node.select('li')
                        ssg_content = [f' * {list.text}' for list in lists]
                        ssg_content = '\n'.join(ssg_content)
                    else : continue
                    ssg_check.append(node.text)
                    ssg_final.append(ssg_content)



            print('\n\n'.join(ssg_final))                           #設計完成，等待進一步處理

except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    # 確保連接關閉
    connection.close()

### 資訊欄
#article_classification 
#article_classification_full 
#comment
#commentauthor
#commentdate
#post_author
#post_content
#post_date
#post_excerpt
#post_title 
#source_page 
#source_site 
#tag
#thumnbnail
#translation_complete


