from web_pages.models import ObjectsGroup


def menu_links(request):
    if '/about-us/' in request.path:
        links = {
            "Who we are": "history",
            "Documents": "documents",
            "Partners and collaboration": "partners",
            "Contacts": "contacts",
        }
    else:
        links = ObjectsGroup.objects.all()

    return {"links": links}


