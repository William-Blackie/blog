from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static

"""
Views used to test and style error handling pages.
"""
def error_500(request, exception=None):
    return render(request, "500.html", {})

def error_404(request, exception=None):
    return render(request, "404.html", {})


"""
Handlers to override the default error behavior.
"""
def handler404(request, *args, **argv):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response


def robots(request):
    content = "\n".join(["User-Agent: *", "Disallow: /search/", "Allow: /"])
    return HttpResponse(content, content_type="text/plain")
