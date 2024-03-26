# Generated by Django 4.2 on 2024-03-26 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('full_name', models.CharField(max_length=128, verbose_name='Full Name')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('thumbnail', models.TextField()),
                ('html_source_code', models.TextField(verbose_name='Html source code')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='goodread.author', verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=128, verbose_name='Genre Title')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('group_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Group Type')),
                ('thumbnail', models.TextField()),
                ('html_source_code', models.TextField(verbose_name='HTML Source Code')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
            },
        ),
        migrations.CreateModel(
            name='SearchByKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('search_type', models.CharField(default='books', max_length=64, verbose_name='Search Type')),
                ('page_count', models.IntegerField(default=5, verbose_name='Page Count')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searches', to='goodread.keyword')),
            ],
            options={
                'verbose_name': 'Search By Keyword',
                'verbose_name_plural': 'Search By Keywords',
            },
        ),
        migrations.CreateModel(
            name='SearchGroupByKeywordItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.TextField(verbose_name='URL')),
                ('is_scraped', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_group_by_keyword_items', to='goodread.group', verbose_name='Group')),
                ('search_by_keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_group_by_keyword_items', to='goodread.searchbykeyword', verbose_name='Search By Keyword')),
            ],
            options={
                'verbose_name': 'Group Search By Keyword Item',
                'verbose_name_plural': 'Group Search By Keyword Items',
            },
        ),
        migrations.CreateModel(
            name='SearchBookByKeywordItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.TextField(verbose_name='URL')),
                ('is_scraped', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_book_by_keyword_items', to='goodread.book', verbose_name='Book')),
                ('search_by_keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_book_by_keyword_items', to='goodread.searchbykeyword', verbose_name='Search By Keyword')),
            ],
            options={
                'verbose_name': 'Book Search By Keyword Item',
                'verbose_name_plural': 'Book Search By Keyword Items',
            },
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated At')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_genres', to='goodread.book')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_genres', to='goodread.genre')),
            ],
            options={
                'verbose_name': 'Book Genre',
                'verbose_name_plural': 'Book Genres',
            },
        ),
    ]