import requests
import pandas as pd
from sqlalchemy import create_engine
def connect_db():
    #return pymysql.connect(host='localhost', user='root', password='12345', port=3306, db='readinghood')
    return create_engine("mysql+pymysql://root:12345@localhost:3306/readinghood?charset=utf8")

def download_img(img_url,s):
    print (img_url)
    r = requests.get(img_url)
    print(r.status_code)
    if r.status_code == 200:
        # pictures are stored in there
        open('./static/books/'+s, 'wb').write(r.content)
        print("done")
    del r

def get_data(name,id):
    name = name.replace(' ', '%20')

    if name=="new" or not name:
        url = "https://api.itbook.store/1.0/new"

    else:
        url = "https://api.itbook.store/1.0/search/" + name
    response = requests.get(url)
    data_value_list=[]

    if response.status_code == 200:
        result = response.json()

        for i in result['books']:
            image_name = "books/"+i["isbn13"]+".png"

            #====================================
            download_img(i['image'],image_name)
            #===================================
            temp = int(float(i['price'][1:]))
            data_value_list.append({
                'books_name': i["title"],
                'books_author': i["isbn13"],
                'books_price': temp if temp > 0 else 20,
                'books_img': image_name,
                'books_description': i['url'],
                'books_category_id':id
            })
    print(data_value_list)
    return data_value_list


def post(name):
    # you need check id in DB before using this
    #=======================================================
    id1=1
    #=======================================================

    data = get_data(name,id1)
    df = pd.DataFrame(data)

    def write_db(conn, df, table_name):

        df.to_sql(table_name, conn, if_exists='append', index=False)


    df2 = pd.DataFrame({"id":id1,"category_name":name,"category_img":"default.png"},index=[0])
    print(1)
    write_db(connect_db(), df2, 'books_bookscategory')
    print(2)
    write_db(connect_db(), df, 'books_booksinfo')
if __name__ == '__main__':

    post("java")