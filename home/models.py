from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.core.fields import StreamField

from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel

from home.blocks import TitleBlock, ButtonBlock, TwoColumnBlock


class ImageWithCaption(models.Model):
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL)

    panels = [
        ImageChooserPanel('image')
    ]

    class Meta:
        abstract = True


class HomePageImage(Orderable, ImageWithCaption):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='gallery')


class HomePage(Page):
    author = models.CharField(max_length=255, null=True)

    body = StreamField([
        ('misc', TitleBlock()),
        ('column', TwoColumnBlock()),
        ('button', ButtonBlock())
    ], null=True)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        StreamFieldPanel('body'),
        InlinePanel('gallery', label="Gallery Images"),
    ]



