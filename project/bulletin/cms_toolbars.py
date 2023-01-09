from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


@toolbar_pool.register
class ExtendAdminMenuToolbar(CMSToolbar):

    def populate(self):
        custom_menu = self.toolbar.get_or_create_menu('custom_menu', 'Пункт меню')
        custom_menu.add_link_item('Показать тестовую страницу', url=reverse('show_admin_custom_page'))