from django import template

register = template.Library()


@register.simple_tag
def paginate_url(value,field_name,urlencode=None):
    url = "?{}={}".format(field_name,value)

    if urlencode:
        #if url has query parameters of filter, it is in urlencode
        # splitting the urlencode at & so that parameters gets separated
        querystring = urlencode.split('&')
        # filtering page parameter from the list
        filtered_querystring = filter(lambda q:q.split('=')[0]!=field_name,querystring)
        #again encoding the list with &
        encoded_querystring = '&'.join(filtered_querystring)
        # joining page parameter with encoded list
        url = '{}&{}'.format(url,encoded_querystring)
    
    return url