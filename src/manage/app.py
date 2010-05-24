#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Core app.
'''

from exweb import context
from exweb import mapping
from exweb import post
from exweb import HttpBadRequestError
from exweb import HttpForbiddenError

import os
import urllib

import manage

@mapping('/register')
def register():
    '''
    show register page if by get, or do register if by post.
    '''
    if context.method=='get':
        return 'register.html', {}
    # handle post:
    form = context.form
    email = form.get('email').strip().lower()
    user = manage.User.all().filter('user_email =', email).get()
    if user is not None:
        return 'register.html', {'error':'Email is already registered.'}
    passwd = form.get('passwd')
    nicename = form.get_escape('nicename').strip()
    user = manage.User(
            user_email = email,
            user_passwd = passwd,
            user_nicename = nicename,
            user_role = get_default_role()
    )
    user.put()
    return '<html><body><h1>Hi, ' + nicename + ', you have registered successfully!</h1></body></html>'

@mapping('/google')
def google():
    '''
    Sign on from google account. If user sign on for the first time, an User 
    object will be created automatically and its password is set to empty.
    
    Returns:
        The redirected url as string.
    '''
    from google.appengine.api import users
    gu = users.get_current_user()
    if not gu:
        raise StandardError()
    context.remove_cookie(manage.COOKIE_AUTO_SIGN_ON)
    email = gu.email().lower()
    nicename = gu.nickname()
    # check if user exist:
    user = manage.get_user_by_email(email)
    if user is None:
        # auto-create new user:
        role = get_default_role()
        if users.is_current_user_admin():
            role = manage.USER_ROLE_ADMINISTRATOR
        user = manage.create_user(role, email, manage.EMPTY_PASSWORD, nicename, '')
    redirect = context.query.get('redirect', '/')
    return 'redirect:' + redirect

@mapping('/signout')
def signout():
    context.remove_cookie(manage.COOKIE_AUTO_SIGN_ON)
    # TODO: when sign in with google, there should be a cookie named 'from_google=True'
    # and sign out from google.
    redirect = '/'
    referer = context.headers.get('Referer')
    if referer is not None:
        if referer.find('/manage/signout')==(-1):
            redirect = referer
    return 'redirect:' + redirect

@mapping('/signin')
def sign_in():
    '''
    handle sign in request and make cookie for track.
    '''
    if context.method=='get':
        redirect = context.query.get('redirect', '/manage/')
        # make sure NOT redirect to signon:
        if redirect.startswith('/manage/signin'):
            redirect = '/manage/'
        model = { 'redirect' : redirect }
        try:
            from google.appengine.api import users
            model['google_url'] = users.create_login_url('/manage/google?redirect=' + urllib.quote(redirect))
        except ImportError:
            pass
        return 'signin.html', model
    # handle post:
    form = context.form
    email = form.get('email').lower()
    passwd = form.get('passwd')
    if passwd==manage.EMPTY_PASSWORD:
        passwd = ''
    redirect = form.get('redirect', '/manage/')
    expires = manage.COOKIE_EXPIRES_MAX
    try:
        expires = int(form.get('expires'))
    except ValueError:
        pass
    user = manage.User.all().filter('user_email =', email).filter('user_passwd =', passwd).get()
    if user is not None:
        key = str(user.key())
        value = manage.make_sign_on_cookie(key, passwd, expires)
        context.set_cookie(manage.COOKIE_AUTO_SIGN_ON, value, expires)
        return 'redirect:' + redirect
    else:
        return 'signin.html', {'error' : 'Invalid email or password.', 'redirect' : redirect}

@post('/upload/$')
def upload(type):
    if context.user is None:
        raise HttpForbiddenError()
    # get photo service:
    provider = manage.get_setting('storage', 'photo_provider', '')
    if not provider:
        return __upload_result(403, '', '', 'You do not configure a photo provider. Go to "Setting", "Storage" to configure a photo provider.')
    settings = manage.get_settings('storage')
    prefix = provider[:-len('PhotoProvider')].replace('.', '_')
    kw = {}
    for key in settings:
        if key.startswith(prefix):
            k = key[len(prefix):]
            v = settings[key]
            if isinstance(k, unicode):
                k = k.encode('utf8')
            if isinstance(v, unicode):
                v = v.encode('utf8')
            kw[k] = v
    try:
        module_name = provider[:-len('.PhotoProvider')]
        mod = __import__(module_name, globals(), locals(), ['PhotoProvider'])
        payload = context.request.get('NewFile')
        url = mod.PhotoProvider.upload(payload, 'title', 'upload from ExpressMe', **kw)
        if 'photo_proxied' in settings and settings['photo_proxied']=='True':
            import util
            url = util.make_proxy(url)
        __upload_result(0, url, 'filename', '')
    except Exception, e:
        __upload_result(1, '', 'filename', 'Upload failed: %s' % str(e))

def __upload_result(err, url, filename, msg):
    resp = '''
    <script type="text/javascript">
    (function(){
      var d=document.domain;
      while (true){
        try{
          var A=window.parent.document.domain;
          break;
        }
        catch(e) {};
        d=d.replace(/.*?(?:\.|$)/,'');
        if (d.length==0) break;
        try{document.domain=d;}
        catch (e){break;}
        }})();
    window.parent.OnUploadCompleted(%d, "%s", "%s", "%s");
    </script>
    ''' % (err, url, filename, msg)
    context.response.out.write(resp)

@mapping('/')
def app_manage():
    '''
    Display manage page.
    '''
    if context.user is None:
        return 'redirect:/manage/signin?redirect=/manage/'
    import appconfig
    role = context.user.user_role
    query = context.query
    app = query.get('app')
    action = query.get('action')
    menu_list = []
    selected_menu = None
    selected_menu_item = None
    for appname in appconfig.apps:
        ms = __install_app_menu(role, appname)
        for m in ms:
            if m.app==app:
                selected_menu = m
                for it in m.items:
                    if it.action==action:
                        selected_menu_item = it
                        break
        menu_list.extend(ms)
    if selected_menu is None and selected_menu_item is None:
        selected_menu = menu_list[0]
        selected_menu_item = menu_list[0].items[0]
    elif selected_menu is None or selected_menu_item is None:
        raise HttpBadRequestError()
    root = os.path.split(os.path.dirname(__file__))[0]
    module = __import__(selected_menu.app + '.appmanage')
    model = module.appmanage.manage_app(context.user, action=selected_menu_item.action)
    if not 'template' in model:
        raise StandardError('var "template" not found in model.')
    panel_path = os.path.join(root, selected_menu.app, model['template'])
    model.update({
            'name' : context.user.user_nicename,
            'menus' : menu_list,
            'panel' : panel_path,
            'app' : selected_menu.app,
            'action' : selected_menu_item.action,
            'template_path' : lambda file : os.path.join(root, selected_menu.app, file),
            'format_datetime' : lambda d : d.strftime('%Y-%m-%d %H:%M:%S'),
            'format_date' : lambda d : d.strftime('%Y-%m-%d'),
            'format_time' : lambda d : d.strftime('%H:%M:%S'),
            'version' : '1.0.1',
    })
    return 'manage.html', model

def __install_app_menu(role, appname):
    #try:
    module = __import__(appname + '.appmanage')
    #except ImportError:
    #    return []
    appmenus = getattr(module.appmanage, 'appmenus', [])
    list = []
    for menuname, menuitems in appmenus:
        menu = __get_visible_menu(role, appname, menuname, menuitems)
        if menu is not None:
            list.append(menu)
    return list

def __get_visible_menu(role, appname, menuname, menuitems):
    if not isinstance(menuname, basestring):
        return None
    if type(menuitems)!=type([]):
        return None
    items = [item for item in menuitems if isinstance(item, manage.AppMenuItem) and item.role>=role]
    if not items:
        return None
    menu = manage.AppMenu(menuname)
    menu.app = appname
    menu.items = items
    return menu

def get_default_role():
    return int(manage.get_setting(
            manage.SETTING_GLOBAL,
            manage.SETTING_GLOBAL_DEFAULT_ROLE,
            `manage.USER_ROLE_SUBSCRIBER`
    ))
