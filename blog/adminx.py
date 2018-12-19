import xadmin
from django.http.response import HttpResponse
from django.utils.translation import gettext as _
from xadmin import views
# Admin.py定义
from xadmin.plugins.actions import BaseActionView

from blog.forms.ArticleForms import ArticleForm
from blog.models import Comment, Article, Column, Label
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
            # {"type": "addform", "model": Article},
        ]

    ]


@xadmin.sites.register(Column)
class ColumnAdmin(object):
    list_display = ('name', 'slug', 'intro', 'created_time')
    list_display_links = ("name",)
    search_fields = ["name"]
    readonly_fields = ['slug']
    free_query_filter = False
    # exclude = ['slug']
    list_per_page = PER_PAGE_SHOW
    model_icon = 'fa fa-tags'

    def save_models(self):
        # self.new_obj.area_company = C.objects.get(user=self.request.user)
        self.new_obj.slug = CommonUtil.cn_to_pinyin(self.new_obj.name)
        super().save_models()


class MaintainInline(object):
    model = Comment
    extra = 1
    style = "accordion"


class ArticleStatusPublishAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "publishArticle"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = _(
        u'修改%(verbose_name_plural)s状态为发布')  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    # action_name = "delete_selected"
    # description = _(u'Delete selected %(verbose_name_plural)s')
    model_perm = 'change'  #: 该 Action 所需权限
    icon = "fa fa-lightbulb-o"

    def do_action(self, queryset):
        rows_updated = queryset.update(publish_status='p')

        return HttpResponse


class ArticleStatusDropAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "dropArticle"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = _(
        u'修改%(verbose_name_plural)s状态为丢弃')  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'  #: 该 Action 所需权限
    icon = "fa fa-minus"

    def do_action(self, queryset):
        rows_updated = queryset.update(publish_status='d')

        return HttpResponse


class ArticleStatusWriteAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "writeArticle"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = _(
        u'修改%(verbose_name_plural)s状态为草稿')  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'  #: 该 Action 所需权限
    icon = 'fa fa-pencil'

    def do_action(self, queryset):
        rows_updated = queryset.update(publish_status='w')

        return HttpResponse


@xadmin.sites.register(Article)
class ArticleAdmin(object):
    list_display = ('title', 'slug', 'author', 'pub_date', 'update_date', 'publish_status')
    list_display_links = ("title",)
    free_query_filter = False
    search_fields = ["title", "slug", "author", "pub_date", "publish_status"]
    list_filter = [
        "publish_status",
    ]
    readonly_fields = ['slug']
    exclude = ['slug']
    # inlines = [MaintainInline]
    ordering = ["pub_date", "publish_status"]
    # list_editable = ['publish_status']
    list_per_page = PER_PAGE_SHOW
    # actions = [BatchChangeAction, ]
    model_icon = 'fa fa-book'
    form = ArticleForm
    actions = [ArticleStatusPublishAction, ArticleStatusDropAction, ArticleStatusWriteAction, ]

    # wizard_form_list = [
    #     ("基本信息", ("title", 'column', 'label', "author")),
    #     ("內容和状态", ('content', 'publish_status'))
    # ]

    """函数作用：使当前登录的用户只能看到自己权限下的文章"""

    def queryset(self):
        qs = query = Article.objects.all()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(author=self.request.user)

    def save_models(self):
        # self.new_obj.area_company = C.objects.get(user=self.request.user)
        self.new_obj.slug = CommonUtil.cn_to_pinyin(self.new_obj.title)
        article = Article()
        #article.content = self.new_obj.
        label_ids = self.get_label_id(self.form_obj.data["label"])
        article.content = self.new_obj.content
        article.column = self.new_obj.column
        article.title = self.new_obj.title
        article.author = self.new_obj.author
        article.publish_status = self.new_obj.publish_status
        article.save()
        article.label.set(label_ids)
        article.save()
        #super().save_models()
        #self.new_obj.label.entry_set.add(label_ids)
        #super().save_models()

    def get_label_id(self, label_names):
        label_names = label_names.replace('，', ',').replace(' ', ',');
        label_names_list = label_names.split(',')
        label_ids = []
        for name in label_names_list:
            name = name.strip()
            if len(name) > 0:
                Label.objects.get_or_create(name=name, slug=CommonUtil.cn_to_pinyin(name))
                # label_ids.append(get_Or_create_result[0].id)
        return Label.objects.filter(name__in=label_names_list)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    global_search_models = [Article]
    menu_style = 'default'  # 'accordion'
    site_title = "夏~管理系统"
    site_footer = "夏~管理系统"


xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(views.BaseAdminView, BaseSetting)
