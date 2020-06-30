# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from hw_8.instagram_parser.items import FollowersItem
from scrapy.loader import ItemLoader
import json
import re
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):

    name = 'instagram'
    allowed_domains = ['instagram.com']

    def __init__(self, parse_users):
        self.start_urls = ['https://instagram.com/']
        self.parse_users = parse_users

    username = ''
    password = ''
    auth_url = 'https://www.instagram.com/accounts/login/ajax/'

    graphql_link = 'https://www.instagram.com/graphql/query/?'

    user_follows__hashes = {
        'followers_hash': 'c76146de99bb02f6415203be841dd25a',
        'follows_hash': 'd04b0a864b4b54837c0d870b0e77e076'
    }

    # Авторизуемся на сайте

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.auth_url,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.username,
                      'enc_password': self.password},
            headers={'X-CSRFToken': csrf_token}
        )

    # Если авторизация прошла успешно отправляем запрос на страницу исследуемого пользователя
    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    # Извлекаем user_id и делаем запрос списка подписчиков или подписок
    def user_data_parse(self, response: HtmlResponse, username):

        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'include_reel': True,
                     'fetch_mutual': True,
                     'first': 24}
        for key, follows_hash in self.user_follows__hashes.items():
            if key == 'follows_hash':
                variables['fetch_mutual'] = False
            elif key == 'followers_hash':
                variables['fetch_mutual'] = True

            follows_link = f'{self.graphql_link}query_hash={follows_hash}&{urlencode(variables)}'

            yield response.follow(
                follows_link,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables),
                           'follows_hash': follows_hash}
            )

    # Извлекаем полный список и данные по подпискам (подписчикам)
    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables, follows_hash):

        j_body = json.loads(response.text)
        user_data = j_body.get('data').get('user')
        if 'edge_followed_by' in user_data:
            edge_follows = user_data.get('edge_followed_by')
        elif 'edge_follow' in user_data:
            edge_follows = user_data.get('edge_follow')

        page_info = edge_follows.get('page_info')

        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            variables['fetch_mutual'] = False
            follows_link = f'{self.graphql_link}query_hash={follows_hash}&{urlencode(variables)}'
            yield response.follow(
                follows_link,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        follows = edge_follows.get('edges')

        for follow in follows:
            follow_info = follow['node']
            loader = ItemLoader(FollowersItem(), response=response)
            loader.add_value('user_id', follow_info['id'])
            loader.add_value('username', follow_info['username'])
            loader.add_value('full_name', follow_info['full_name'])
            loader.add_value('profile_image', follow_info['profile_pic_url'])
            loader.add_value('is_private', follow_info['is_private'])
            loader.add_value('user_data', follow_info)
            if 'edge_followed_by' in user_data:
                loader.add_value('follow_username', username)
            elif 'edge_follow' in user_data:
                loader.add_value('follower_username', username)

            yield loader.load_item()

    def fetch_user_id(self, text, username):
        matched = re.search('{"id":\"\\d+","username":"%s"}' % username, text).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(':').pop().replace(r'"', '')