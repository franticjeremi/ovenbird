# -*- coding: utf-8 -*-
'''
Created on 20 мая 2016 г.

@author: gudach
'''
from .base import Base
import requests

class Vk(Base):

    def handler_auth(self):
        self._response = requests.get(
        "https://oauth.vk.com/authorize?client_id=5478254&scope=friends,photos,status,wall,groups,messages,email,notifications,stats,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.37&response_type=token")
    
    def send_message(self, user_id=None, message="Test message"):
        self._response = requests.get('https://api.vk.com/method/messages.send',
                            params={'user_id': user_id, 
                                    'message': message, 
                                    'access_token': self._token
                            })
        
    def get_groups_admin(self, user_id=None):
        self._response = requests.get('https://api.vk.com/method/groups.get',
                            params={'user_id': user_id, 
                                    'extended': 1, 
                                    'filter':'admin', 
                                    'access_token': self._token
                            })
        
    def groups_search(self, query, offset=0, count=10):
        self._response = requests.get('https://api.vk.com/method/groups.search',
                            params={'q': query, 
                                    'offset': offset, 
                                    'count': count,  
                                    'access_token': self._token
                            })
        
    def get_group_members(self, group_id, offset=0, count=10):
        self._response = requests.get('https://api.vk.com/method/groups.getMembers',
                            params={'group_id': group_id, 
                                    'offset': offset, 
                                    'count': count,
                                    'fields': 'can_write_private_message,can_send_friend_request',
                                    'access_token': self._token
                            })
        
    def get_user_info(self, user_id):
        self._response = requests.get('https://api.vk.com/method/users.get',
                            params={'user_ids': user_id,
                                    'fields': 'can_write_private_message,can_send_friend_request'
                            })
        
    def request_friend(self, user_id, text):
        self._response = requests.get('https://api.vk.com/method/friends.add',
                            params={'user_is': user_id,
                                    'text': text
                            })
        
    def group_invite(self, user_id, group_id):
        self._response = requests.get('https://api.vk.com/method/groups.invite',
                            params={'user_is': user_id,
                                    'group_id': group_id
                            })
        
    def create_album(self, title, group_id, description=''):
        self._response = requests.get('https://api.vk.com/method/photos.createAlbum',
                            params={'title': title,
                                    'group_id': group_id,
                                    'description': description,
                                    'upload_by_admins_only': 1,
                                    'privacy_view': 'friends',
                                    'privacy_comment': 'friends'
                            })
        
    def upload_photo(self, album_id, group_id):
        self._response = requests.get('https://api.vk.com/method/photos.getUploadServer',
                            params={'album_is': album_id,
                                    'group_id': group_id
                            })
        
    def post_wall(self, owner_id, message):
        self._response = requests.get('https://api.vk.com/method/wall.post',
                            params={'from_group': 1,
                                    'owner_id': owner_id,
                                    'message': message,
                            })
        
    def pin_wall(self, owner_id, post_id):
        self._response = requests.get('https://api.vk.com/method/wall.pin',
                            params={'owner_id': owner_id,
                                    'post_id': post_id,
                            })
        
    