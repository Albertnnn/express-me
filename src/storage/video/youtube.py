#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Manage videos on YouTube.
'''

import StringIO

import gdata.photos.service
from storage import Provider
from storage import ProviderSetting

# default developer key registered by dev@expressme.org, 
# but you can also specify your developer key so that you can track the API call on: 
# http://code.google.com/apis/youtube/dashboard/
DEFAULT_DEVELOPER_KEY = 'AI39si76YKqh2z4yW6Xe1astvsuR1fcUVQPx_6Ilxfbk3T7mwaaQM7T841lNHO1tulDufk3vdyu0Cj2TfhYb2HHzZ73csTssnA'

class PhotoProvider(Provider):
    name = 'Google PicasaWeb'
    description = 'Using Google PicasaWeb as your photo storage service.'
    settings = [
            ProviderSetting('email', True, 'PicasaWeb Login Email'),
            ProviderSetting('passwd', True, 'PicasaWeb Login Password', is_password=True),
    ]

    @staticmethod
    def upload(payload, title, summary='', default_dir=None, **kw):
        if not title:
            title = 'unamed'
        pc = PicasaClient(kw['email'], kw['passwd'])
        if default_dir is not None:
            # TODO: need find out the album named as 'default_dir'...
            pass
        uploaded = pc.upload_photo(StringIO.StringIO(payload), title, summary)
        return uploaded.content.src

class PicasaClient(object):
    def __init__(self, email, passwd):
        '''Init picasa client.
        
        email: user's email address.
        base64_passwd: password with base64 encoding.
        '''
        self.gd_client = gdata.photos.service.PhotosService(email, passwd)
        self.gd_client.ProgrammaticLogin()

    def get_albums(self):
        '''Get all albums of user.
        
        return album list.
        '''
        return self.gd_client.GetUserFeed().entry

    def get_album(self, title, auto_create=False):
        '''Get album by title.
        
        title: album title as string.
        auto_create: create album automatically if album not found, default to False.
        
        return album object.
        '''
        albums = self.gd_client.GetUserFeed()
        for album in albums.entry:
            if album.title.text==title:
                return album
        if auto_create:
            return self.create_album(title)
        raise StandardError('Album not found: ' + title)

    def create_album(self, title, summary=''):
        '''Create a new album.
        
        title: album title as string.
        summary: album summary as string, default to ''.
        
        return album class.
        '''
        return self.gd_client.InsertAlbum(title, summary)

    def get_photos(self, album=None):
        '''Get photos of an album.
        
        album: album object, default to None.
        
        return photo list.
        '''
        album_id = 'default'
        if album is not None:
            album_id = album.gphoto_id.text
        return self.gd_client.GetFeed('/data/feed/api/user/default/albumid/%s?kind=photo' % (album_id,)).entry

    def upload_photo(self, input, title, summary='', album=None):
        '''Upload a new photo
        
        input: file-like object, usually a StringIO object.
        title: photo title as string.
        summary: photo summary as string, default to ''.
        album: album object that contains uploaded photo, default to None.
        
        return photo object.
        '''
        album_id = 'default'
        if album is not None:
            album_id = album.gphoto_id.text
        album_url = '/data/feed/api/user/default/albumid/%s' % (album_id)
        return self.gd_client.InsertPhotoSimple(album_url, title, summary, input)

def upload(payload, username, passwd, title, summary='', default_dir=None):
    '''
    Upload a photo.
    
    Args:
        payload: bytes of uploaded photo as a raw string.
        username: username to sign on picasaweb.
        passwd: password to sign on picasaweb.
    
    Returns:
        The uploaded photo's URL as string.
    '''
    if not title:
        title = 'unamed'
    pc = PicasaClient(username, passwd)
    if default_dir is not None:
        # TODO: need find out the album named as 'default_dir'...
        pass
    uploaded = pc.upload_photo(StringIO.StringIO(payload), title, summary)
    return uploaded.content.src
