# -*- coding: utf-8 -*-
from elasticsearch_dsl import Document, Completion, Keyword, Text,Date,Boolean
from elasticsearch_dsl.analysis import CustomAnalyzer as CustomAnaly
from elasticsearch_dsl.connections import connections


class CustomAnalyzer(CustomAnaly):
    def get_analysis_definition(self):
        return {}


class SearchType(Document):
    url = Keyword()
    url_origin = Keyword()
    title = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    img_download = Keyword()
    is_index=Boolean()
    create_date = Date()
    save_data=Date()
    suggest = Completion(analyzer=CustomAnalyzer("ik_max_word", filter=["lowercase"]))
    class Index:
        name = 'hfut_search'

    class Meta:
        doc_type = 'hfut_type'


class SearchPicSave(Document):
    img_name=Keyword()
    img_path=Keyword()
    save_data=Date()
    class Index:
        name = 'hfut_pic'

    class Meta:
        doc_type = 'hfut_pic_type'

if __name__ == "__main__":
    params={
        "host": "localhost",
        "port": 16110
    }
    connections.create_connection(**params)
    SearchType.init()
    SearchPicSave.init()
