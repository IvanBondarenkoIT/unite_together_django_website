from web_pages.models import ObjectsGroup
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.db.models import CharField


def generate_url(group_name, slug):
    return Concat(Value(f"/{group_name}/"), F("slug"), output_field=CharField())


def menu_links(request):
    if "/about-us/" in request.path:
        links = {
            "Про нас": "who_we_are",
            "Документи": "documents",
            "Партнери та співпраця": "partners",
            "Контакти": "contact",
        }
        return {"links": links}

    page_name = None

    if "/events/" in request.path:
        page_name = "events"
    elif "/projects/" in request.path:
        page_name = "projects"

    if page_name:
        links = (
            ObjectsGroup.objects.filter(page__name=page_name)
            .order_by("order")
            .annotate(pre_computed_url=generate_url(page_name, F("slug")))
        )
    else:
        links = (
            ObjectsGroup.objects.all()
            .order_by("order")
            .annotate(pre_computed_url=generate_url(page_name, F("slug")))
        )

    return {"links": links}
