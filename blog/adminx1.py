import xadmin
from xadmin import views

# Admin.py定义
from xadmin.plugins.batch import BatchChangeAction

from blog.admin import ArticleAdmin
from blog.models2 import Comment, Article, Column
from lawerWeb.settings import PER_PAGE_SHOW
from utils.commonUtil import CommonUtil


@xadmin.sites.register(views.website.IndexView)
class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "夏~",
             "content": "<h3> Welcome to 夏~! </h3><p></p>"},
            # {"type": "chart", "model": "app.accessrecord", "chart": "user_count",
            #  "params": {"_p_date__gte": "2013-01-08", "p": 1, "_p_date__lt": "2013-01-29"}},
            # {"type": "list", "model": "app.host", "params": {"o": "-guarantee_date"}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start",
             "btns": [{"model": Article}]},
            #{"type": "addform", "model": Article},
        ]

    ]

@xadmin.sites.register(Column)
class ColumnAdmin(object):
    list_display = ('name', 'slug', 'intro', 'created_time')
    list_display_links = ("name",)
    search_fields = ["name"]
    readonly_fields = ['slug']
    #exclude = ['slug']
    list_per_page = PER_PAGE_SHOW
    model_icon = 'fa fa-tags'


    def save_models(self):
        #self.new_obj.area_company = C.objects.get(user=self.request.user)
        self.new_obj.slug = CommonUtil.cn_to_pinyin(self.new_obj.name)
        super().save_models()


class MaintainInline(object):
    model = Comment
    extra = 1
    style = "accordion"

@xadmin.sites.register(Article)
class ArticleAdmin(object):
    list_display = ('title', 'slug', 'author', 'pub_date', 'update_date', 'publish_status')
    list_display_links = ("title",)

    search_fields = ["title", "slug", "author", "pub_date", "publish_status"]
    list_filter = [
        "publish_status",
    ]
    readonly_fields = ['slug']
    exclude = ['slug']
    inlines = [MaintainInline]
    ordering = ["pub_date", "publish_status"]
    list_per_page = PER_PAGE_SHOW
    #actions = [BatchChangeAction, ]
    model_icon = 'fa fa-book'

    wizard_form_list = [
        ("基本信息", ("title", 'column', 'label', "author")),
        ("內容和状态", ('content', 'publish_status'))
    ]

    """函数作用：使当前登录的用户只能看到自己权限下的文章"""
    def queryset(self):
        qs = query = Article.objects.all()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(author=self.request.user)


    # def save_models(self):
    #     #self.new_obj.area_company = C.objects.get(user=self.request.user)
    #     #self.new_obj.slug = CommonUtil.cn_to_pinyin(self.new_obj.title)
    #     super().save_models()


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    global_search_models = [Article]
    menu_style = 'default'  # 'accordion'
    site_title = "夏~管理系统"
    site_footer = "@夏~管理系统"


xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(views.BaseAdminView, BaseSetting)
