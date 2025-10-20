from django.conf import settings


def adsense_settings(request):
    """Expose AdSense settings to templates.

    - ADSENSE_AD_CLIENT: client id (ca-pub-...)
    - ADSENSE_AD_SLOT: optional ad unit id
    """
    return {
        'ADSENSE_AD_CLIENT': getattr(settings, 'ADSENSE_AD_CLIENT', ''),
        'ADSENSE_AD_SLOT': getattr(settings, 'ADSENSE_AD_SLOT', ''),
    }
