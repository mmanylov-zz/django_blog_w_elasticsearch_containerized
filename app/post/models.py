from django.db import models
from django.utils import timezone
import markdown 
from .search import PostType
import dateutil.parser


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("ЧПУ", max_length=255, unique=True)
    excerpt = models.TextField("Выдержка")
    # minutes_to_read = models.IntegerField("ETA")
    body = models.TextField("Текст", blank=True)
    markdown = models.TextField("Markdown")
    minutes_to_read = models.IntegerField("Minutes to read")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    published_at = models.DateTimeField("Опубликовано", default=timezone.now)
    status = models.CharField("Статус", max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    @property
    def views(self):
        return ViewCount.objects.filter(post=self).count()

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-published_at',)

    def publish(self):
        self.published_at = timezone.now()
        self.status = 'published'
        super(Post, self).save()

    def save(self, *args, **kwargs):
        self.body = markdown.markdown(self.markdown, extensions=['markdown.extensions.extra', 'markdown.extensions.nl2br', 'markdown.extensions.sane_lists'])
        super(Post, self).save(*args, **kwargs)

    def increment_view_counter(self, ip):
        ViewCount(post=self, ip=ip).save()

    def __str__(self):
        return self.title

    def indexing(self):
        obj = PostType(
            meta={'id': self.id},
            published_at=self.published_at.strftime("%b, %d %Y"),
            title=self.title,
            text=self.body,
            excerpt=self.excerpt,
            slug=self.slug,
            minutes_to_read=self.minutes_to_read,
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class ViewCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    first_visit_date = models.DateTimeField("Первый просмотр", auto_now_add=True)
