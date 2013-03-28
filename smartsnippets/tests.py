from django.test import TestCase
from utils import regex_replace

class TestITSRename(TestCase):

    def test1(self):

        CONTENT_INITIAL = """
                        THIS ONE WILL BE RENAMED !!!!
        {% load blabla, its_image_resize, bla %}
        its_image_resize
        <a href="{{ topic1.url }}"><img src="{{ topic1.image|its_image_resize:"226x" }}" alt="{{ topic1.title }}" /></a>

        <div class="funder-image">
                                             THIS ONE WILL BE RENAMED !!!!
        <a href="{{ logo05_url }}"><img src="{{ logo05|its_image_resize:"136x" }}" height="45"></a>
        </div>

        {{ logo5|its_image_resize: }} -- here there is no width and height
        {{ logo5|its_image_resize:"165" }} -- here there is no x
        {{ logo5|its_image_resize "165" }} -- here there is no :
        {{ logo5 its_image_resize:"165x" }} -- here there is no |
        { logo5|its_image_resize:"165x" }} -- here there is no starting {
        logo5|its_image_resize:"165x" }} -- here there is no starting {{
        """

        CONTENT_MIGRATED = """
                        THIS ONE WILL BE RENAMED !!!!
        {% load blabla, image_resize, bla %}
        its_image_resize
        <a href="{{ topic1.url }}"><img src="{{ topic1.image|its_image_resize:"226x" }}" alt="{{ topic1.title }}" /></a>

        <div class="funder-image">
                                             THIS ONE WILL BE RENAMED !!!!
        <a href="{{ logo05_url }}"><img src="{{ logo05|image_resize:"136x" }}" height="45"></a>
        </div>

        {{ logo5|its_image_resize: }} -- here there is no width and height
        {{ logo5|its_image_resize:"165" }} -- here there is no x
        {{ logo5|its_image_resize "165" }} -- here there is no :
        {{ logo5 its_image_resize:"165x" }} -- here there is no |
        { logo5|its_image_resize:"165x" }} -- here there is no starting {
        logo5|its_image_resize:"165x" }} -- here there is no starting {{
        """

        self.assertEquals(CONTENT_MIGRATED,
                          regex_replace(CONTENT_INITIAL, "its_image_resize", "image_resize", ["logo05"]))
