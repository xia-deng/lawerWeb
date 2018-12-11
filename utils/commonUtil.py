from django.db.models import QuerySet
from xpinyin import Pinyin


class CommonUtil:
    @staticmethod
    def toString(Obj):
        objtype=type(Obj)
        print(objtype)


    @staticmethod
    def querySetToList(querySet,field=""):
        if(type(querySet)==QuerySet):
            list=[]
            list=[', '.join(x) for x in querySet]
            return list
        return None


    @staticmethod
    def cn_to_pinyin(cn_words):
        return Pinyin().get_pinyin(cn_words).replace('-','').lower()



