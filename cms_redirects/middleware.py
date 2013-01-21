from cms_redirects.models import CMSRedirect
from django import http
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def get_redirect(old_path):
    try:
        r = CMSRedirect.objects.get(site__id__exact=settings.SITE_ID,
                                    enabled=True,
                                    old_path=old_path)
    except CMSRedirect.DoesNotExist:
        r = None
    return r


def remove_slash(path):
    return path[:path.rfind('/')]+path[path.rfind('/')+1:]


def remove_query(path):
    return path.split('?', 1)[0]


class RedirectFallbackMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, http.Http404):

            # First try the whole path.
            path = request.get_full_path()
            r = get_redirect(path)

            # It could be that we need to try without a trailing slash.
            if r is None and settings.APPEND_SLASH:
                r = get_redirect(remove_slash(path))

            # It could be that the redirect is defined without a query string.
            if r is None and path.count('?'):
                r = get_redirect(remove_query(path))

            # It could be that we need to try without query string and without a trailing slash.
            if r is None and path.count('?') and settings.APPEND_SLASH:
                r = get_redirect(remove_slash(remove_query(path)))


            if r is not None:
                if r.soft:
                    redirect_url = r.page.get_absolute_url() if r.page else r.new_path
                    return render_to_response('cms_redirects/soft_redirect.html',
                                             {'redirect': r, 'redirect_url': redirect_url},
                                             context_instance=RequestContext(request))
                if r.page:
                    if r.response_code == '302':
                        return http.HttpResponseRedirect(r.page.get_absolute_url())
                    else:
                        return http.HttpResponsePermanentRedirect(r.page.get_absolute_url())
                if r.new_path == '':
                    return http.HttpResponseGone()
                if r.response_code == '302':
                    return http.HttpResponseRedirect(r.new_path)
                else:
                    return http.HttpResponsePermanentRedirect(r.new_path)


