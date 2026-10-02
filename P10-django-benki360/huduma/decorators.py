from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def linahitaji_jukumu(*majukumu):
    """Authz: mtumiaji lazima awe na kundi (group) mojawapo au superuser.

    Analogia: mlinzi wa mlango wa ofisi - anajua kila mlango una
    kadi gani (admin, mpokeaji, mhasibu).
    """
    def _pambo(ndege):
        @wraps(ndege)
        def _kifungu(request, *a, **kw):
            if not request.user.is_authenticated:
                return redirect("ingia")
            if (request.user.is_superuser
                    or request.user.groups.filter(
                        name__in=majukumu).exists()):
                return ndege(request, *a, **kw)
            raise PermissionDenied(
                "Huna ruhusa ya ukurasa huu (unahitaji: %s)"
                % ", ".join(majukumu))
        return _kifungu
    return _pambo
