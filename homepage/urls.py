from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from homepage import settings

ROBOTS_TXT_CONTENT = """\
User-Agent: *
Disallow: /

User-agent: GPTBot
Disallow: /
"""


@require_GET
def robots_txt(
    request,
):
    return HttpResponse(ROBOTS_TXT_CONTENT, content_type="text/plain")


@require_GET
@cache_control(max_age=60, immutable=True, public=True)
def favicon_file(request):
    name = request.path.lstrip("/")
    file = (settings.BASE_DIR / "homepage" / "static" / "favicons" / name).open("rb")
    return FileResponse(file)


@require_GET
def font_file(request):
    name = request.path.lstrip("/")
    file = (settings.BASE_DIR / "homepage" / "static" / "fonts" / name).open("rb")
    return FileResponse(file)


@require_GET
def home(request):
    return render(request, "home.html")


@require_GET
def work(request):
    return render(request, "work.html")


@require_GET
def contact(request):
    return render(request, "contact.html")


urlpatterns = [
    path("robots.txt", robots_txt),
    path("android-chrome-192x192.png", favicon_file),
    path("android-chrome-512x512.png", favicon_file),
    path("apple-touch-icon.png", favicon_file),
    path("browserconfig.xml", favicon_file),
    path("favicon-16x16.png", favicon_file),
    path("favicon-32x32.png", favicon_file),
    path("favicon.ico", favicon_file),
    path("mstile-150x150.png", favicon_file),
    path("site.webmanifest", favicon_file),
    path("RobotoMono-Regular.woff", font_file),
    path("RobotoMono-Regular.woff2", font_file),
    path("", home, name="home"),
    path("work", work, name="work"),
    path("contact", contact, name="contact")
]
