# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""
for more info on media pipelines visit -
https://doc.scrapy.org/en/latest/topics/media-pipeline.html
"""

# useful for handling different item types with a single interface

# install Pillow first for the ImagesPipeline to work correctly


import os
import sqlite3
from sqlite3 import OperationalError as OE

from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class MalImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={
            'title': item["anime_title"][0],
            'rating': item["personal_rating"][0]
        })  # because "anime_title", "personal_rating" returns a list
                for x in item.get('image_urls', [])]
        # use file_urls to customize files pipeline

    def file_path(self, request, response=None, info=None):
        image_name = request.meta['title'].replace(":", "").replace("/", " ")
        return 'ScrapedImages/%s.jpg' % image_name

    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_name = request.meta['image_name'].replace(":", "").replace("/", " ")
        return 'ScrapedImages_thumb/%s.jpg' % image_name


# edit num of instances of column_data_list[n] based on "n=len(column_data_list)"
# for multiple lists within column_data_list use for loop while calling sqlite_store


class SQLitePipeline(object):

    def __init__(self):
        self.DB_name = "MAL"
        self.conn = sqlite3.connect(f"{self.DB_name}.sqlite")
        self.cur = self.conn.cursor()
        self.table_name = "Completed_Anime"
        self.column_names_list = ["Anime_Title", "Score", "Media_Path", "Media_Type"]
        self.data_types_list = ["text", "text", "text", "text"]
        self.create_table()

    def create_table(self):
        self.cur.executescript(f"""
            DROP TABLE IF EXISTS {self.table_name};
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE);
            """)
        try:
            for n in range(len(self.column_names_list)):
                col_name = self.column_names_list[n]
                data_type = self.data_types_list[n]
                self.cur.executescript(f"""
                ALTER TABLE {self.table_name}
                ADD {col_name} {data_type};
                """)
        except OE:
            pass
        self.conn.commit()

    def process_item(self, item, spider):
        store_path = item["images"][0]["path"]
        anime_title = item['anime_title'][0]
        my_rating = item["personal_rating"][0]
        media_type = "Image"
        path = os.path.join(os.getcwd(), store_path)
        column_data_list = [anime_title, my_rating, path, media_type]
        col_names = ", ".join(self.column_names_list)
        n_v = []
        for _ in range(len(self.column_names_list)):
            n_v.append("?")
        num_of_values = ", ".join(n_v)

        self.cur.execute(f'''INSERT OR IGNORE INTO {self.table_name} ({col_names}) VALUES ({num_of_values})''',
                         (column_data_list[0], column_data_list[1], column_data_list[2], column_data_list[3])
                         )

        self.conn.commit()
        return item
