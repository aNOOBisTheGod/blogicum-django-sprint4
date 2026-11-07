"""Publication models for the Blogicum site."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PublishedModel(models.Model):
    """Common publication state and creation timestamp."""

    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        """Keep this base model out of the database."""

        abstract = True


class Category(PublishedModel):
    """A thematic group of publications."""

    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор', unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.'),
    )

    class Meta:
        """Localized category names and deterministic ordering."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        """Display the category title in admin forms."""
        return self.title


class Location(PublishedModel):
    """An optional geographic label for publications."""

    name = models.CharField('Название места', max_length=256)

    class Meta:
        """Localized location names."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        """Display the location name in admin forms."""
        return self.name


class Post(PublishedModel):
    """A publication with an author, category and optional location."""

    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    image = models.ImageField('Изображение', upload_to='posts/', blank=True)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'),
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор публикации',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='posts', verbose_name='Категория',
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='posts', verbose_name='Местоположение',
    )

    class Meta:
        """Display the newest publications first."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', '-pk')

    def __str__(self):
        """Display the publication title in the admin site."""
        return self.title


class Comment(models.Model):
    """A comment belonging to a publication and its author."""

    text = models.TextField('Текст комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        """Show comments in chronological order."""

        ordering = ('created_at', 'pk')
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Show a short comment preview."""
        return self.text[:50]
