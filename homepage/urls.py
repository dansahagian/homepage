from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from homepage import settings

ROBOTS_TXT_CONTENT = """\
User-agent: GPTBot
Disallow: /

# OpenAI, ChatGPT
# https://platform.openai.com/docs/gptbot
User-agent: GPTBot
Disallow: /

# Google AI (Bard, etc)
# https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers
User-agent: Google-Extended
Disallow: /

# Block common crawl
# I have mixed feelings on this one, but many models are trained on this data
# It is also used to bootstrap new search indices though
# https://commoncrawl.org/ccbot
User-agent: CCBot
Disallow: /

# Facebook
# https://developers.facebook.com/docs/sharing/bot/
User-agent: FacebookBot
Disallow: /

# Cohere.ai
# https://darkvisitors.com/agents/cohere-ai
User-agent: cohere-ai
Disallow: /

# Perplexity
# https://docs.perplexity.ai/docs/perplexitybot
User-agent: PerplexityBot
Disallow: /

# Anthropic
# https://darkvisitors.com/agents/anthropic-ai
User-agent: anthropic-ai
Disallow: /

# ...also anthropic
# https://darkvisitors.com/agents/claudebot
User-agent: ClaudeBot
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
    return redirect("https://linkedin.com/in/dansahagian")


@require_GET
def email(request):
    return render(request, "email.html")


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
    path("email", email, name="email"),
    path("work", work, name="work")
]
