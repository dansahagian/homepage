from django import forms
from django.http import FileResponse
from django.shortcuts import redirect, render, reverse
from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from homepage.settings import BASE_DIR, ENV


class ContactForm(forms.Form):
    math_question = forms.IntegerField(
        required=True,
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Your Email Address"}),
    )
    message = forms.CharField(
        required=True,
        max_length=1024,
        widget=forms.Textarea(attrs={"placeholder": "Your Message to Dan"}),
    )


# def send_email(email, message):
#     message = f"{email}\n\n{message}"
#     msg = MIMEText(message)
#     msg["Subject"] = "Website Contact Form"
#     msg["From"] = SMTP_SENDER
#     msg["To"] = SMTP_SENDER
#
#     conn = smtplib.SMTP_SSL(SMTP_SERVER)
#     conn.login(SMTP_USER, SMTP_PASSWORD)
#     try:
#         conn.sendmail(SMTP_SENDER, [SMTP_SENDER], msg.as_string())
#     finally:
#         conn.quit()


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


def get_theme_context(request):
    current_theme = request.session.get("theme", None)
    if current_theme is None:
        request.session["theme"] = "dark"

    return {"theme": request.session["theme"]}


@require_GET
def home(request):
    context = get_theme_context(request)
    return render(request, "home.html", context=context)


@require_GET
def about(request):
    context = get_theme_context(request)
    return render(request, "about.html", context=context)


@require_GET
def work(request):
    context = get_theme_context(request)
    return render(request, "work.html", context=context)


def contact(request):
    if request.method == "GET":
        context = get_theme_context(request)
        context["form"] = ContactForm()
        return render(request, "contact.html", context=context)

    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #
    #     if form.is_valid():
    #         math_question = form.cleaned_data["math_question"]
    #         email = form.cleaned_data["email"]
    #         message = form.cleaned_data["message"]
    #
    #         if math_question == 3:
    #             send_email(email, message)
    #             return render(request, "contact_success.html")
    #         else:
    #             return render(request, "contact_failure.html")
    #
    #     return redirect(reverse("home"))


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


def error_404(request, exception):
    return render(request, "404.html", status=404)


handler404 = error_404

urlpatterns = [
    path("", home, name="home"),
    path("about", about, name="about"),
    path("work", work, name="work"),
    path("contact", contact, name="contact"),
    path("theme", theme, name="theme"),
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
