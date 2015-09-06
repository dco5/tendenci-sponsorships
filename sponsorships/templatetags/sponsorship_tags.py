from django.template import Library

register = Library()


@register.inclusion_tag("sponsorships/nav.html", takes_context=True)
def sponsorship_nav(context, user, sponsorship=None):
    context.update({
        'nav_object': sponsorship,
        "user": user
    })
    return context


@register.inclusion_tag("sponsorships/top_nav_items.html", takes_context=True)
def sponsorship_current_app(context, user, sponsorship=None):
    context.update({
        'app_object': sponsorship,
        "user": user
    })
    return context


@register.inclusion_tag("sponsorships/search-form.html", takes_context=True)
def sponsorship_search(context):
    return context