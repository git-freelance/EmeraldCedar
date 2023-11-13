from core.models import SiteConfiguration


def siteconfig(request):
    return {'site_config': SiteConfiguration.get_solo()}
