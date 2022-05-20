


from account.models import Settings


def get_context(request):
    settings_object,created = Settings.objects.get_or_create(id=1,defaults={'organization_name':'SMART CARD NEPAL','organization_address':'Dharan,Sunsari','toll_amount':100})

    context = {
        'settings':settings_object
    }

    return context
