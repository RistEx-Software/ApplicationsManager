from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from docutils.core import publish_parts
from django.core.cache import cache
from django.template import loader
from django.conf import settings
import os

def page(request, path):
	key = 'ApplicationsManager.apps.doc.page.%s' % (path.replace('/', '.'))
	ctx = cache.get(key)
	# Do not cache when debugging.
	if not ctx or settings.DEBUG:
		filePath = os.path.join(settings.DOCS_ROOT, path)
		print("Attempting to load doc file %s" % filePath)

		# "index" is the document representing its parent
		# directory. We canonicalize URLs here such that they
		# never include "index".
		#
		if os.path.basename(filePath) == 'index':
			return HttpResponseRedirect("..")
		if os.path.isdir(filePath):
			filePath = os.path.join(filePath, 'index')
		if not os.path.isfile(filePath):
			raise Http404

		ctx = render(request, 'docs/doc.html',
		{
			# Render docutils parts
			'parts': publish_parts(
				source=open(filePath).read(),
				writer_name="html4css1",
				settings_overrides={
					'cloak_email_addresses': True,
					'initial_header_level': 2,
				},
			),
		})
		cache.set(key, ctx)
	return ctx
