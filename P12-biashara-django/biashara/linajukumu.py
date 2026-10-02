from functools import wraps

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def linahitaji_jukumu(*majukumu):
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
                "Huna ruhusa (unahitaji: %s)" % ", ".join(majukumu))
        return _kifungu
    return _pambo


class MauzajiWaBidhaa(LoginRequiredMixin):
    """CBV: kuuza/simamia bidhaa ni kazi ya MUUZAJI (au admin)."""

    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated
                and not (request.user.is_superuser
                         or request.user.groups.filter(
                             name="muuzaji").exists())):
            raise PermissionDenied(
                "Kuuza bidhaa ni kazi ya MUUZAJI")
        return super().dispatch(request, *args, **kwargs)
