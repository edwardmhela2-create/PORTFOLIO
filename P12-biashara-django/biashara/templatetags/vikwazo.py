from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def yupo_jukumu(context, *majukumu):
    user = context["request"].user
    return (user.is_superuser
            or user.groups.filter(name__in=majukumu).exists())
