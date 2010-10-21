'''
Base functions and classes.
'''

DEPRECATED = True

__author__ = 'Michael Liao'

class Setting():

    def __init__(self, key, value, default=None):
        if not isinstance(key, str):
            raise ValueError('Key must be str in Setting')
        if len(key)==0 or len(key)>=100:
            raise ValueError('Key must be str in 1-100 chars in Setting')
        self.key = key
        self.value = value
        if default is not None:
            self.default = default

class IntegerSetting(Setting):

    def __init__(self, key, value, default=None):
        if type(value)!=int:
            raise ValueError('Value must be integer in IntegerSetting')
        if default is not None and type(default)!=int:
            raise ValueError('Default must be integer in IntegerSetting')
        super(IntegerSetting, self).__init__(key, str(value), default)

class StringSetting(Setting):

    def __init__(self, key, value, default=None):
        if not isinstance(value, basestring):
            raise ValueError('Value must be basestring in StringSetting')
        if default is not None and not isinstance(value, basestring):
            raise ValueError('Default must be basestring in StringSetting')
        super(StringSetting, self).__init__(key, value, default)

class PasswordSetting(StringSetting):
    ' The same as StringSetting but display as password '

    def __init__(self, key, value, default=None):
        super(PasswordSetting, self).__init__(key, value, default)

class SelectSetting(Setting):
    '''
    Makes a setting value in the provided select options.
    '''

    def __init__(self, key, select_dict, default=None):
        if type(select_dict)!=dict:
            raise ValueError('Select_dict must be dict in SelectSetting')
        if default is not None and not default in select_dict:
            raise ValueError('Default must be in dict in SelectSetting')
        self.select_dict = select_dict
        super(SelectSetting, self).__init__(key, default, default)
