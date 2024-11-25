from django.shortcuts import redirect, render, reverse
from django.views.decorators.http import require_GET
from user_agents import parse

from homepage.core.models import RequestLog


def get_theme_context(request):
    current_theme = request.session.get("theme", None)
    if current_theme is None:
        request.session["theme"] = "dark"

    return {"theme": request.session["theme"]}


def log_request(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    ua = parse(request.META.get("HTTP_USER_AGENT", ""))

    try:
        RequestLog.objects.create(
            path=request.path,
            user_agent=ua.ua_string,
            ip_address=xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", ""),
            ua_browser_family=ua.browser.family,
            ua_browser_version=ua.browser.version_string,
            ua_device_family=ua.device.family,
            ua_device_model=ua.device.model,
        )
    except:  # noqa
        pass


@require_GET
def home(request):
    log_request(request)

    context = get_theme_context(request)
    return render(request, "home.html", context=context)


@require_GET
def about(request):
    log_request(request)

    context = get_theme_context(request)
    return render(request, "about.html", context=context)


@require_GET
def work(request):
    log_request(request)

    context = get_theme_context(request)
    return render(request, "work.html", context=context)


@require_GET
def contact(request):
    log_request(request)

    context = get_theme_context(request)
    return render(request, "contact.html", context=context)


@require_GET
def theme(request):
    current_theme = request.session.get("theme", None)
    referer = request.META.get("HTTP_REFERER")

    if current_theme is None:
        return redirect(reverse("home"))

    request.session["theme"] = "light" if current_theme == "dark" else "dark"
    if referer:
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect(reverse("home"))
