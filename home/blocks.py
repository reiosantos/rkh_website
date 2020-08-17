from copy import deepcopy

from django.core.exceptions import ValidationError
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from home.validators import validate_title


class TwoColumnBlock(blocks.StructBlock):
    paragraph = blocks.RichTextBlock(help_text="Your body content")
    image = ImageChooserBlock(help_text="Attach any image", required=True)

    class Meta:
        template = 'home/blocks/two_column.html'
        icon = 'placeholder'
        label = 'Two Columns'


class TitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(classname="full title", help_text="Blog Heading", validators=[validate_title])
    sub_title = blocks.RichTextBlock(help_text="Page sub-content")

    def clean(self, value):
        val = super(TitleBlock, self).clean(value)

        sub_title = deepcopy(val.get('sub_title')).source.lower()
        title = deepcopy(val.get('title')).lower()

        tt_arr = list(set(title.split()))
        stt_arr = list(set(sub_title.strip("<p>/").split()))

        for word in tt_arr:
            if word in stt_arr:
                errors = {
                    'sub_title': [f'Subtitle should not contain any words used in the title. It includes `{word}`']
                }
                raise ValidationError('Validation error in StructBlock', params=errors)

        return val

    class Meta:
        template = "home/blocks/title.html"
        icon = 'edit'
        label = "Title and Sub title"


# class MultipleImageChooserBlock(blocks.StructBlock):
#     images = blocks.ListBlock(ImageChooserBlock())
#
#     class Meta:
#         template = "home/blocks/images.html"
#         icon = 'photo'
#         label = "Gallery"


class ButtonBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, max_length=20)
    page = blocks.PageChooserBlock(required=False, classname="page-block")
    url = blocks.URLBlock(required=False, classname="url-block")
    use_page = blocks.BooleanBlock(required=False, help_text="Check if you want to link to internal page")

    class Meta:
        template = "home/blocks/button.html"
        icon = 'edit'
        label = "Page Action"
        form_template = 'home/blocks/button_form.html'
