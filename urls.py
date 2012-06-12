from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^boleto/', include('django-boleto.boleto.urls')),
    url(r'^boleto_bb/$', 'django-boleto.boleto.views.boleto_bb'),
	url(r'^boleto_caixa/$', 'django-boleto.boleto.views.boleto_caixa'),
	url(r'^boleto_real/$', 'django-boleto.boleto.views.boleto_real'),
	url(r'^boleto_bradesco/$', 'django-boleto.boleto.views.boleto_bradesco'),
)

import os
urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', 
        	{'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)