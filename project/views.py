from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
from django.conf import settings

from project.models import VimeoUser


def ajax_user_details(request):
    """
    AJAX View to give the results for related search key after applying filters
    """
    paying = request.POST.get('paying', '')
    search = request.POST.get('search', '')
    uploaded = request.POST.get('uploaded', '')
    staffpick = request.POST.get('staff', '')
    total = 0
    users = None
    if search:
        users = cache.get('%s_searched_users_%s_%s_%s' % (search, paying, uploaded, staffpick), None)
        if users is None:
            if search.startswith('^'):
                users = VimeoUser.objects.filter(name__istartswith=search[1:])
            elif search.startswith('='):
                users = VimeoUser.objects.filter(name__iexact=search[1:])
            else:
                users = VimeoUser.objects.filter(name__icontains=search)
            if paying:
                users = users.filter(paying=True)
            if uploaded:
                users = users.filter(video=True)
            if staffpick:
                users = users.filter(staffpick=True)
            cache.add('%s_searched_users_%s_%s_%s' % (search, paying, uploaded, staffpick), users,
                      settings.SEARCH_CACHE_TIME)
        if users:
            total = users.count()
            users = users[:100]
    con = dict(
        total=total,
        users=users,
    )
    return render_to_response('profiles/users.html', con, RequestContext(request))


def index(request, template_name="profiles/index.html", **kwargs):
    context = RequestContext(request)
    return render_to_response(template_name, kwargs, context)
