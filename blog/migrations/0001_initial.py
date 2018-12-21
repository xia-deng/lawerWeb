# Generated by Django 2.1.3 on 2018-12-20 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('slug', models.CharField(db_index=True, editable=False, max_length=128, verbose_name='文章索引')),
                ('content', froala_editor.fields.FroalaField(verbose_name='内容')),
                ('publish_status', models.CharField(choices=[('d', '丢弃'), ('p', '发布'), ('w', '草稿')], default='w', max_length=1, verbose_name='状态')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Article_Read_Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('records_count', models.IntegerField(default=0, verbose_name='阅读数')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56, verbose_name='栏目名称')),
                ('slug', models.CharField(db_index=True, max_length=128, verbose_name='栏目索引')),
                ('intro', models.CharField(default='', max_length=512, verbose_name='栏目简介')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '文章类别',
                'ordering': ['created_time'],
                'verbose_name_plural': '文章类别',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128, null=True)),
                ('content', models.CharField(max_length=500)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56, verbose_name='主题名称')),
                ('slug', models.CharField(db_index=True, max_length=128, verbose_name='主题索引')),
                ('intro', models.CharField(default='', max_length=512, verbose_name='主题简介')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '标签',
                'ordering': ['created_time'],
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128, null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='文章')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='评论')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('record_date', models.DateTimeField(auto_now_add=True, verbose_name='记录时间')),
                ('operation', models.CharField(choices=[('r', '访问'), ('c', '评论'), ('p', '点赞'), ('o', '其他')], max_length=1, verbose_name='动作')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Column', verbose_name='文章类别'),
        ),
        migrations.AddField(
            model_name='article',
            name='label',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Label', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='read_records',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.Article_Read_Records'),
        ),
    ]
