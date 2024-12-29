# from django.shortcuts import get_object_or_404
# from web_pages.models import Events  # Убедитесь, что модель Events импортирована
#
#
# class LastEventMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if (
#                 "/events/" in request.path
#                 and request.headers.get("X-Requested-With") != "XMLHttpRequest"
#             ):
#                 # Получаем часть пути после "/events/"
#                 event_slug = request.path.split("/events/")[-1].strip("/")
#                 event_slug = event_slug.split("/")[-1]
#                 if event_slug:  # Проверяем, что slug существует
#                     print(f"event_slug: {event_slug}")  # Печатаем slug (event_slug)
#                     try:
#                         # Ищем событие по slug
#                         event = get_object_or_404(Events, slug=event_slug)
#                         # Сохраняем данные в сессию
#                         request.session["last_event"] = {
#                             "url": request.path,
#                             "name": event.name,
#                             "thumbnail": (event.image.url if event.image else None),
#                         }
#                         print(f"event_slug: {event_slug}")  # Печатаем slug (event_slug)
#                     except Events.DoesNotExist:
#                         pass  # Если событие не найдено, ничего не делаем
#         return self.get_response(request)
