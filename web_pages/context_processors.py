from web_pages.models import ObjectsGroup


def menu_links(request):
    links = ObjectsGroup.objects.all()
    return {"links": links}
