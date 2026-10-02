from django import template

register = template.Library()


@register.simple_tag
def yupo_jukumu(user, *majukumu):
    """Authz kwenye template: je, mtumiaji ana kundi lolote kati ya hawa?"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=majukumu).exists()
