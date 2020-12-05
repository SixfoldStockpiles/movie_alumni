from typing import List, Any, Tuple, Optional
from collections import Counter

from data_classes import Config, TVWithCount, MovieWithCount
from tmdb_client import TmdbClient


class MovieAlumni:
    def __init__(self, tmdb_client: TmdbClient, top_n_tv_show_cast: int = 25) -> None:
        self._tmdb_client = tmdb_client
        self._top_n_tv_show_cast = top_n_tv_show_cast

    def get_most_overlapping_cast_movies_and_tv(self, title: str, n: int = 10) -> Tuple[List[TVWithCount], List[MovieWithCount]]:
        secondary_tv_ids: List[int] = []
        secondary_movie_ids: List[int] = []

        tv_ids = self._tmdb_client.find_tv(title)        
        for tv_id in tv_ids:
            cast_ids = self._tmdb_client.find_tv_cast(tv_id, top_n=self._top_n_tv_show_cast)
            for cast_id in cast_ids:
                secondary_movie_ids += self._tmdb_client.movies_for_person(cast_id)
                secondary_tv_ids += self._tmdb_client.tv_for_person(cast_id)

        movie_ids = self._tmdb_client.find_movie(title)
        for movie_id in movie_ids:
            cast_ids = self._tmdb_client.find_movie_cast(movie_id)
            for cast_id in cast_ids:
                secondary_movie_ids += self._tmdb_client.movies_for_person(cast_id)
                secondary_tv_ids += self._tmdb_client.tv_for_person(cast_id)

        counter_secondary_tv = Counter(secondary_tv_ids)
        counter_secondary_movie = Counter(secondary_movie_ids)

        return (
            [TVWithCount(title=self._tmdb_client.get_tv(tv_id)['name'], count=count) 
             for tv_id, count in counter_secondary_tv.most_common(n)], 
            [MovieWithCount(title=self._tmdb_client.get_movie(movie_id)['original_title'], count=count) 
             for movie_id, count in counter_secondary_movie.most_common(n)],
        )


if __name__ == '__main__':
    config = Config.load()

    tmdb_client = TmdbClient(config.api_key)
    finder = MovieAlumni(tmdb_client)
    title = 'it\'s always sunny in philadelphia'
    tv_shows, movies = finder.get_most_overlapping_cast_movies_and_tv(title)
    for tv_show in tv_shows:
        print(tv_show)
    for movie in movies:
        print(movie)
