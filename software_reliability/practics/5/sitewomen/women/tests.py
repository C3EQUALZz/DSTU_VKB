from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from women.models import Women, Category, TagPost, Husband, UploadFiles


class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']

    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], "Главная страница")

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], w[:5])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerysetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        "Действия после выполнения каждого теста"

User = get_user_model()


class WomenModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Создаем категорию
        cls.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Создаем теги
        cls.tag1 = TagPost.objects.create(tag='Tag 1', slug='tag-1')
        cls.tag2 = TagPost.objects.create(tag='Tag 2', slug='tag-2')

        # Создаем мужа
        cls.husband = Husband.objects.create(
            name='Test Husband',
            age=40
        )

        # Создаем опубликованную запись
        cls.published_woman = Women.objects.create(
            title='Published Post',
            slug='published-post',
            content='Test content',
            is_published=Women.Status.PUBLISHED,
            cat=cls.category,
            author=cls.user
        )
        cls.published_woman.tags.add(cls.tag1)

        # Создаем черновик
        cls.draft_woman = Women.objects.create(
            title='Draft Post',
            slug='draft-post',
            content='Draft content',
            is_published=Women.Status.DRAFT,
            cat=cls.category,
            author=cls.user
        )

    def test_create_women(self):
        """Тест создания записи"""
        self.assertEqual(self.published_woman.title, 'Published Post')
        self.assertEqual(self.published_woman.slug, 'published-post')
        self.assertEqual(self.published_woman.is_published, Women.Status.PUBLISHED)
        self.assertEqual(self.published_woman.cat.name, 'Test Category')
        self.assertEqual(self.published_woman.author.username, 'testuser')
        self.assertEqual(list(self.published_woman.tags.all()), [self.tag1])

    def test_str_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.published_woman), 'Published Post')

    def test_get_absolute_url(self):
        """Тест получения абсолютного URL"""
        expected_url = reverse('post', kwargs={'post_slug': 'published-post'})
        self.assertEqual(self.published_woman.get_absolute_url(), expected_url)

    def test_published_manager(self):
        """Тест кастомного менеджера published"""
        published_posts = Women.published.all()
        self.assertIn(self.published_woman, published_posts)
        self.assertNotIn(self.draft_woman, published_posts)

    def test_slug_validation(self):
        """Тест валидации длины slug"""
        # Слишком короткий slug (менее 5 символов)
        with self.assertRaises(ValidationError) as context:
            Women.objects.create(
                title='Short Slug',
                slug='shrt',
                cat=self.category,
                author=self.user
            ).full_clean()

        self.assertIn('Минимум 5 символов', str(context.exception))

    def test_unique_slug(self):
        """Тест уникальности slug"""
        with self.assertRaises(IntegrityError):
            Women.objects.create(
                title='Duplicate Slug',
                slug='published-post',  # Используем существующий slug
                cat=self.category,
                author=self.user
            )

    def test_photo_field(self):
        """Тест необязательного поля фото"""
        woman = Women.objects.create(
            title='No Photo',
            slug='no-photo',
            cat=self.category,
            author=self.user
        )
        # Проверяем, что поле photo не содержит файла
        self.assertFalse(woman.photo)
        self.assertIsNone(woman.photo.name)

    def test_relationships(self):
        """Тест связей между моделями"""
        # Связь с категорией
        self.assertEqual(self.published_woman.cat, self.category)
        self.assertIn(self.published_woman, self.category.posts.all())

        # Связь с тегами
        self.published_woman.tags.add(self.tag2)
        self.assertEqual(self.published_woman.tags.count(), 2)
        self.assertIn(self.published_woman, self.tag1.tags.all())

        # Связь с мужем
        self.published_woman.husband = self.husband
        self.published_woman.save()
        self.assertEqual(self.published_woman.husband, self.husband)
        self.assertEqual(self.husband.wuman, self.published_woman)

        # Связь с автором
        self.assertEqual(self.published_woman.author, self.user)
        self.assertIn(self.published_woman, self.user.posts.all())

    def test_meta_options(self):
        """Тест мета-опций модели"""
        meta = Women._meta
        self.assertEqual(meta.verbose_name, 'Известные женщины')
        self.assertEqual(meta.verbose_name_plural, 'Известные женщины')
        self.assertEqual(meta.ordering, ['-time_create'])
        self.assertTrue(any(index.fields == ['-time_create'] for index in meta.indexes))


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_create_category(self):
        """Тест создания категории"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')

    def test_str_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.category), 'Test Category')

    def test_get_absolute_url(self):
        """Тест получения абсолютного URL"""
        expected_url = reverse('category', kwargs={'cat_slug': 'test-category'})
        self.assertEqual(self.category.get_absolute_url(), expected_url)

    def test_meta_options(self):
        """Тест мета-опций модели"""
        meta = Category._meta
        self.assertEqual(meta.verbose_name, 'Категория')
        self.assertEqual(meta.verbose_name_plural, 'Категории')


class TagPostModelTest(TestCase):
    def setUp(self):
        self.tag = TagPost.objects.create(
            tag='Test Tag',
            slug='test-tag'
        )

    def test_create_tag(self):
        """Тест создания тега"""
        self.assertEqual(self.tag.tag, 'Test Tag')
        self.assertEqual(self.tag.slug, 'test-tag')

    def test_str_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_get_absolute_url(self):
        """Тест получения абсолютного URL"""
        expected_url = reverse('tag', kwargs={'tag_slug': 'test-tag'})
        self.assertEqual(self.tag.get_absolute_url(), expected_url)


class HusbandModelTest(TestCase):
    def setUp(self):
        self.husband = Husband.objects.create(
            name='Test Husband',
            age=40
        )

    def test_create_husband(self):
        """Тест создания мужа"""
        self.assertEqual(self.husband.name, 'Test Husband')
        self.assertEqual(self.husband.age, 40)
        self.assertEqual(self.husband.m_count, 0)

    def test_str_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.husband), 'Test Husband')

    def test_optional_age(self):
        """Тест необязательного поля возраста"""
        husband = Husband.objects.create(name='No Age Husband')
        self.assertIsNone(husband.age)

    def test_default_marriage_count(self):
        """Тест значения по умолчанию для количества браков"""
        husband = Husband.objects.create(name='Default Count Husband')
        self.assertEqual(husband.m_count, 0)


class UploadFilesModelTest(TestCase):
    def test_create_upload_file(self):
        """Тест создания файла"""
        upload = UploadFiles.objects.create(
            file='uploads_model/test.txt'  # Указываем полный путь
        )
        self.assertEqual(upload.file.name, 'uploads_model/test.txt')