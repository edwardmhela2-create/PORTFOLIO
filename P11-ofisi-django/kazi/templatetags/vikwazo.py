from django import template

register = template.Library()


@register.simple_tag
def yupo_jukumu(user, *majukumu):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=majukumu).exists()
