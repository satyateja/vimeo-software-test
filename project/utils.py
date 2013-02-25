from __future__ import unicode_literals
import requests
from requests.auth import OAuth1
import simplejson as json
from django.conf import settings

from project.models import VimeoUser


def vimeo_authentication(data):
    """
    This function will authenticate the API call for vimeo and return the response in JSON format
    """
    auth = OAuth1(settings.APP_KEY, settings.APP_SECRET, settings.AUTH_TOKEN, settings.AUTH_SECRET,
                  signature_type='auth_header')
    client = requests.session(headers=None, auth=auth, proxies=None)
    func = getattr(client, 'get')
    try:
        response = func('https://vimeo.com/api/rest/v2', params=data)
        content = json.loads(response._content)
    except Exception, e:
        return None
    return content


def get_vimeo_users(category, page, total):
    """
    This function will get all users of a category on a particular page and returns no.of users saved.
    """
    data = dict(
        format=u'json',
        method=u'vimeo.categories.getRelatedPeople',
        category=category,
        page=page,
    )
    count = 0
    if total and total < 50:
        data['per_page'] = total
    content = vimeo_authentication(data)
    if content and content.get('users') and content['users'].get('user'):
        users = content['users']['user']
        for user in users:
            vimeo_user, created = VimeoUser.objects.get_or_create(vimeo_id=user['id'])
            if created:
                vimeo_user.name = user.get('display_name', '')
                vimeo_user.url = user.get('profileurl', '')
                vimeo_user.paying = bool(int(user.get('is_plus', '0')) or int(user.get('is_pro', '0')))
                vimeo_user.staffpic = bool(int(user.get('is_staff', '0')))
                if settings.UPLOADED_VIDEO_STATUS:
                    vimeo_user.video = get_vimeo_user_video_status(user['id'])
                vimeo_user.save()
                print '.'
                count += 1
        print '\n'
    return count


def get_vimeo_categories():
    """
    This function will get all categories of vimeo and get users for each category and store it into DB.
    """
    data = dict(
        format=u'json',
        method=u'vimeo.categories.getAll',
    )
    content = vimeo_authentication(data)
    if content and content.get('stat', '') == 'ok' and int(content['categories']['total']) > 0:
        total = settings.SEARCH_USERS_TOTAL
        print 'Starting to Crawl Vimeo Users. It will take a while (3Hrs/5000 users approx) please be patient'
        for category in content['categories']['category']:
            total_users = category.get('total_users')
            category_name = category.get('word')
            if total_users and category_name:
                total_users = int(total_users)
                page = 1
                while total_users and total and page * 50 < total_users:
                    count = get_vimeo_users(category_name, page, total)
                    page += 1
                    total_users -= count
                    total -= count
        print '%s Users from vimeo were crawled successfully' % settings.SEARCH_USERS_TOTAL


def get_vimeo_user_video_status(uid):
    """
    This function will give whether there are uploaded videos for given user
    """
    data = dict(
        format=u'json',
        method=u'vimeo.people.getInfo',
        user_id=uid,
    )
    content = vimeo_authentication(data)
    has_videos = False
    if content and content.get('stat', '') == 'ok' and content.get('person', ''):
        has_videos = bool(content['person'].get('number_of_uploads'))
    return has_videos