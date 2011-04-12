#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Twitter Widget that display latest tweets and a 'follow me' link.
'''

from random import randint

from google.appengine.api import urlfetch
from google.appengine.runtime import apiproxy_errors

import widget

IGNORE_HEADERS = frozenset([
    'set-cookie',
    'expires',
    'cache-control',
    # Ignore hop-by-hop headers
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade'
])

class Widget(widget.WidgetModel):
    '''
    Show recent tweets
    '''
    __title__ = 'Recent Tweets'
    __author__ = 'Michael Liao'
    __description__ = 'Show your recent tweets'
    __url__ = 'http://www.expressme.org/'

    @staticmethod
    def get_settings():
        return [
                widget.WidgetSetting(key='username', description='Twitter username', required=True, default=''),
                widget.WidgetSetting(key='recent_tweets', description='How many recent tweets to display', required=True, default='20'),
        ]

#    title = widget.WidgetSetting()
#    username = widget.WidgetSetting()
#    recent_tweets = widget.WidgetSetting()
#    show_follow_me = widget.WidgetSetting()

    def get_content__raw__(self):
        self.cache = '600'
        id = 'tw_' + self.__id__
        url = 'http://api_twitter_com/1/statuses/user_timeline/%s.json%%3Fcount=%s?__cache__=%s' % (self.username, self.recent_tweets, self.cache)
        return r'''<div id="%s"><em>Loading...</em></div>
<script type="text/javascript">
if (typeof(g_widget_recent_tweets) == "undefined") {

  g_widget_recent_tweets = new Object();

  g_widget_recent_tweets.parse_text = function(text){
    var re_at = /\@[a-zA-Z0-9]+/;
    var re_sharp = /\#[a-zA-Z0-9]+/;
    var re_http = /https?\:\/\/[a-zA-Z0-9\_\-\.\/\%%\?\&\#\=]+/; // NOTE the escape of 'percent' in Python
    var buffer = "";
    while (true) {
      var s_at = text.match(re_at);
      var s_sharp = text.match(re_sharp);
      var s_http = text.match(re_http);
      if (s_at==null && s_sharp==null && s_http==null) {
        buffer = buffer + text;
        break;
      }
      var p_at = s_at==null ? text.length : text.indexOf(s_at[0]);
      var p_sharp = s_sharp==null ? text.length : text.indexOf(s_sharp[0]);
      var p_http = s_http==null ? text.length : text.indexOf(s_http[0]);
      var min = Math.min(p_at, p_sharp, p_http);
      buffer = buffer + text.substring(0, min);
      if (min==p_at) {
        text = text.substring(min + s_at[0].length);
        var user = s_at[0].substring(1);
        buffer = buffer + "@" + "<a href=\"https://twitter.com/" + user + "\" target=\"_blank\">" + user + "</a>";
      }
      else if (min==p_sharp) {
        text = text.substring(min + s_sharp[0].length);
        var q = s_sharp[0].substring(1);
        buffer = buffer + "#" + "<a href=\"http://twitter.com/search?q=%%23" + q + "\" target=\"_blank\">" + q + "</a>";
      }
      else if (min==p_http) {
        text = text.substring(min + s_http[0].length);
        buffer = buffer + "<a href=\"" + s_http[0] + "\" target=\"_blank\">" + s_http[0] + "</a>";
      }
    }
    return buffer;
  }

  g_widget_recent_tweets.parse_date = function(text){
    // format: Tue Mar 02 02:16:15 +0000 2010
    var _months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var ss = text.split(" ");
    var Y = parseInt(ss[5], 10);
    // month:
    var M = 0;
    for (var i=0; i<_months.length; i++){
      if(_months[i]==ss[1]){
        M = i;
        break;
      }
    }
    // day:
    var D = parseInt(ss[2], 10);
    // time:
    var tt = ss[3].split(":");
    // hour:
    var h = parseInt(tt[0], 10);
    // minute:
    var m = parseInt(tt[1], 10);
    // second:
    var s = parseInt(tt[2], 10);
    // create date:
    var utc = Date.UTC(Y, M, D, h, m, s, 0);
    var nowd = new Date();
    var now = Date.UTC(nowd.getUTCFullYear(), nowd.getUTCMonth(), nowd.getUTCDate(), nowd.getUTCHours(), nowd.getUTCMinutes(), nowd.getUTCSeconds(), 0);
    // diff:
    var diff = Math.round((now - utc) / 60000);
    if (diff<=1)
      return "about 1 minute ago";
    if (diff<60)
      return "about " + diff + " minutes ago";
    diff = Math.round(diff / 60);
    if (diff<=1)
      return "about 1 hour ago";
    if (diff<24)
      return "about " + diff + " hours ago";
    diff = Math.round(diff / 24);
    if (diff<=1)
      return "about 1 day ago";
    if (diff<=30)
      return "about " + diff + " days ago";
    return _months[M] + " " + D + this.get_th(D);
  }

  g_widget_recent_tweets.get_th = function(a){
    if (a==1 || a==11 || a==21 || a==31)
      return "st";
    if (a==2 || a==12 || a==22)
      return "nd";
    if (a==3 || a==13 || a==23)
      return "rd";
    return "th";
  }

  g_widget_recent_tweets.create_request = function(url){
    if (window.XMLHttpRequest){
      return new XMLHttpRequest();
    }
    if (window.ActiveXObject){
      return new ActiveXObject("Microsoft.XMLHTTP");
    }
    return null;
  }

  g_widget_recent_tweets.async_call = function(url, success, failure){
    req = this.create_request(url);
    req.onreadystatechange = function() {
      if (this.readyState==4){
        if (this.status==200){
          success(this.responseText);
        }
        else{
          failure(this.status);
        }
      }
    }
    req.open("GET", url);
    req.send(null);
  }

  g_widget_recent_tweets.get_tweets = function(url, username, dom_id){
    this.async_call("/util/proxy/" + url,
      function(text){
        data = eval(text);
        var s = "";
        if (data.error) {
          s = "<p style=\"text-indent:0;color:red\">" + data.error + "</p>";
        }
        else {
          for (i=0; i<data.length; i++){
            st = data[i];
            s = s + "<p style=\"text-indent:0\">" + g_widget_recent_tweets.parse_text(st.text) + "<br/><span style=\"color:#666;font-size:0.9em;font-style:italic\">" + g_widget_recent_tweets.parse_date(st.created_at) + " via " + st.source + "</span></p>";
          }
          s = s + "<p style=\"text-indent:0\"><a href=\"https://twitter.com/" + username + "\" target=\"_blank\">Follow Me!</a></p>";
        }
        document.getElementById(dom_id).innerHTML = s;
      },
      function(errorCode){
        document.getElementById(dom_id).innerHTML = "<p style=\"text-indent:0;color:red\">Error (" + errorCode + ") in get tweets.</p>";
      }
    );
  }
}
// make an async call:
g_widget_recent_tweets.get_tweets("%s", "%s", "%s");
</script>
        ''' % (id, url, self.username, id)
