import xadmin
from django.http.response import HttpResponse
from django.utils.translation import gettext as _
from xadmin import views
# Admin.py定义
from xadmin.plugins.actions import BaseActionView

from blog.forms.ArticleForms import ArticleForm
from blog.models import Comment, Article, Column, Label, Poll
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
    reversion_enable = True

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

    def comments_records(self, instance):
        return Comment.objects.filter(article=instance.id).count()

    comments_records.short_description = "评论数"
    comments_records.allow_tags = True
    comments_records.is_column = True

    def poll_records(self, instance):
        return Poll.objects.filter(article=instance.id).count()

    poll_records.short_description = "点赞数"
    poll_records.allow_tags = True
    poll_records.is_column = True

    list_display = ('title', 'slug', 'author', 'pub_date', 'update_date', 'read_records', 'comments_records', 'poll_records', 'publish_status')
    list_display_links = ("title",)
    free_query_filter = False
    search_fields = ["title", "slug", "author", "pub_date", "publish_status"]
    list_filter = [
        "publish_status",
    ]
    grid_layouts = ("table", "thumbnails")
    show_detail_fields = []
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

    # list_editable = (
    #     "title", "publish_status"
    # )
    # wizard_form_list = [
    #     ("基本信息", ("title", 'column', 'label', "author")),
    #     ("內容和状态", ('content', 'publish_status'))
    # ]
    #style_fields = {"publish_status" : "radio-inline"}

    """函数作用：使当前登录的用户只能看到自己权限下的文章"""

    def queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.query_by_user(self.request.user.id)

    def save_models(self):
        # self.new_obj.area_company = C.objects.get(user=self.request.user)
        self.new_obj.slug = CommonUtil.cn_to_pinyin(self.new_obj.title)
        article = Article()
        #article.content = self.new_obj.
        label_ids = self.get_label_id(self.form_obj.cleaned_data["label"])
        #self.new_obj.label.set(None)
        # article.content = self.new_obj.content
        # article.column = self.new_obj.column
        # article.title = self.new_obj.title
        # article.author = self.new_obj.author
        # article.publish_status = self.new_obj.publish_status
        #created_article = Article.objects.create(content= self.new_obj.content, column=self.new_obj.column, title= self.new_obj.title, author=self.new_obj.author, publish_status=self.new_obj.publish_status)
        #super().save_models()
        #for label in label_ids:
        #    created_article.label.add(label)
        #created_article.save()
        #article.save()
        #super().save_models()
        self.form_obj.cleaned_data["label"] = label_ids
        self.new_obj.save()
        self.new_obj.label.set(label_ids)
        #super().save_models()
        #self.new_obj.save()

    def get_field_attrs(self, db_field, **kwargs):
       return super().get_field_attrs(db_field, **kwargs)

    def get_label_id(self, label_names):
        label_names = label_names.replace('，', ',').replace(' ', ',');
        label_names_list = label_names.split(',')
        labels = []
        for name in label_names_list:
            name = name.strip()
            if len(name) > 0:
                temp_result = Label.objects.get_or_create(name=name, slug=CommonUtil.cn_to_pinyin(name), intro= name)
                # label_ids.append(get_Or_create_result[0].id)
                labels.append(temp_result[0].id)
        return labels


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
