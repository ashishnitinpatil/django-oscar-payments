# -*- coding: utf-8 -*-

"""
.. module:: oscar_payments.apps.checkout.app
   :platform: Unix
   :synopsis: TODO

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""
import logging
from collections import OrderedDict
from django.conf import settings
from django.conf.urls import url, include
from oscar.apps.checkout import app
from oscar_payments import try_import
from oscar_payments.apps.checkout.views import PaymentDetailsView


class CheckoutApplication(app.CheckoutApplication):
    payment_details_view = PaymentDetailsView

    def __init__(self, *args, **kwargs):
        super(CheckoutApplication, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("%s.%s" % (self.__class__.__module__,
                                                self.__class__.__name__))
        self._modules = None

    def get_urls(self):
        base_urls = super(CheckoutApplication, self).get_urls()
        urls = []
        for module in self.modules.values():
            urls.append(url(module['url'], include(module['app'].urls)))
        return urls + base_urls

    @property
    def modules(self):
        """
        Populate and return registered payment modules

        :return: An OrderedDict like { module_name -> { 'url': url,
                                                        'app': application }}
        """
        if self._modules is None:
            self._modules = OrderedDict()
            for root, appname in settings.OSCAR_PAYMENT_MODULES:
                app = try_import(appname + '.app')
                if app is not None:
                    application = app.application
                    self._modules[application.name] = {'url': root,
                                                       'app': application}
                else:
                    self.log.warning("Oscar misconfigured! %s.app cannot be "
                                     "imported", appname)

        return self._modules


application = CheckoutApplication()
