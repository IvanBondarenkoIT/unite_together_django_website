from django.core.cache import cache
from .models import Contacts

def contacts_processor(request):
    """
    Context processor that provides contact information to all templates.
    The data is cached for 1 hour to reduce database queries.
    """
    CACHE_KEY = 'contacts_data'
    contacts = cache.get(CACHE_KEY)
    
    if not contacts:
        try:
            # Get the first active contact entry
            contacts = Contacts.objects.filter(status=True).first()
            if contacts:
                # Cache for 1 hour (3600 seconds)
                cache.set(CACHE_KEY, contacts, 3600)
        except:
            contacts = None
    
    return {
        'contacts': contacts
    }
