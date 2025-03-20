from django.http import FileResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from homepage.core.views import fmoney, home, projects, signal, theme, work
from homepage.settings import BASE_DIR, ENV


@require_GET
@cache_control(max_age=60, immutable=True, public=True)
def favicon_file(request):
    name = request.path.lstrip("/")
    file = (BASE_DIR / "homepage" / "static" / "favicons" / name).open("rb")
    return FileResponse(file)


@require_GET
def font_file(request):
    name = request.path.lstrip("/")
    file = (BASE_DIR / "homepage" / "static" / "fonts" / name).open("rb")
    return FileResponse(file)


def error_404(request, exception):
    return render(request, "404.html", status=404)


handler404 = error_404

urlpatterns = [
    path(route="", view=home, name="home"),
    path(route="work", view=work, name="work"),
    path(route="projects", view=projects, name="projects"),
    path(route="fmoney", view=fmoney, name="fmoney"),
    path(route="signal", view=signal, name="signal"),
    path(route="theme", view=theme, name="theme"),
]

if ENV == "dev":
    local_urls = [
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
    ]

    urlpatterns = urlpatterns + local_urls
