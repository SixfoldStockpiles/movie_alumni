from typing import List, Any, Tuple, Optional
from dataclasses import dataclass

import requests

from data_classes import TVWithCount, MovieWithCount


class TmdbClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key     

        self._base = 'https://api.themoviedb.org/3'

    def find_movie(self, title: str) -> List[int]:
        page = 1
        num_pages = 1
        ids: List[int] = []
        endpoint = 'search/movie'

        while page <= num_pages:
            response = requests.get(f'{self._base}/{endpoint}?query={title}&include_adult=false&page={page}&api_key={self._api_key}')
            
            if response.status_code != 200:
                raise ValueError(f'API failure: {response.text}')

            num_pages = response.json()['total_pages']
            ids.extend([item['id'] for item in response.json()['results'] if item['original_title'].lower() == title.lower()])
            page += 1

        return ids

    def find_tv(self, title: str) -> List[int]:
        page = 1
        num_pages = 1
        ids: List[int] = []
        endpoint = 'search/tv'

        while page <= num_pages:
            response = requests.get(f'{self._base}/{endpoint}?query={title}&include_adult=false&page={page}&api_key={self._api_key}')
            
            if response.status_code != 200:
                raise ValueError(f'API failure: {response.text}')

            num_pages = response.json()['total_pages']
            ids.extend([item['id'] for item in response.json()['results'] if item['original_name'].lower() == title.lower()])
            page += 1

        return ids

    def find_movie_cast(self, movie_id: int) -> List[int]:
        endpoint = f'movie/{movie_id}/credits'

        page = 1
        num_pages = 1
        ids: List[int] = []

        while page <= num_pages:
            response = requests.get(f'{self._base}/{endpoint}?api_key={self._api_key}')
            if response.status_code != 200:
                raise ValueError(f'API failure: {response.text}')

            num_pages = response.json()['total_pages']

            page += 1

            print([(person['id'], person['name'], person['character']) for person in response.json()['cast']])
            ids.extend([person['id'] for person in response.json()['cast']])

        return ids

    def find_tv_cast(self, tv_id: int, top_n: Optional[int] = 25) -> List[int]:
        endpoint = f'tv/{tv_id}/aggregate_credits'

        response = requests.get(f'{self._base}/{endpoint}?api_key={self._api_key}')
        if response.status_code != 200:
            raise ValueError(f'API failure: {response.text}')

        cast = sorted(response.json()['cast'], key=lambda person: person['total_episode_count'], reverse=True)
        if top_n is not None:
            cast = cast[:top_n]
        return [person['id'] for person in cast]

    def movies_for_person(self, person_id: int) -> List[int]:
        endpoint = f'person/{person_id}/movie_credits'
        response = requests.get(f'{self._base}/{endpoint}?api_key={self._api_key}')
        if response.status_code != 200:
            raise ValueError(f'API failure: {response.text}')
        return [movie['id'] for movie in response.json()['cast']]

    def tv_for_person(self, person_id: int) -> List[int]:
        endpoint = f'person/{person_id}/tv_credits'
        response = requests.get(f'{self._base}/{endpoint}?api_key={self._api_key}')
        if response.status_code != 200:
            raise ValueError(f'API failure: {response.text}')
        return [movie['id'] for movie in response.json()['cast']]

    def get_movie(self, movie_id: int) -> Any:
        endpoint = f'movie/{movie_id}'
        response = requests.get(f'{self._base}/{endpoint}?api_key={self._api_key}')
        if response.status_code != 200:
            raise ValueError(f'API failure: {response.text}')
        return response.json()

    def get_tv(self, tv_id: int) -> Any:
        endpoint = f'tv/{tv_id}'
        response = requests.get(f'{self._base}/{endpoint}?api_key={self._api_key}')
        if response.status_code != 200:
            raise ValueError(f'API failure: {response.text}')
        return response.json()
