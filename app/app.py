import requests

from zipfile import ZipFile

import sys


import csv

import logging

from models import Movie

from elasticsearch import Elasticsearch



from elasticsearch.helpers import bulk



def connect_elastic(elastic_url):
    return Elasticsearch(elastic_url)


def gen_movie_docs(movies: list[Movie], index_name: str):
    for movie in movies:
        yield {
            "_index": index_name,
            "title": movie.title,
            "year": movie.year,
            "genres": movie.genres
        }






def download_and_unzip_dataset():
    filename = "ml-latest-small.zip"

    file_path = f"temp/{filename}"

    url_dataset = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    
    try:
        resp = requests.get(url_dataset, allow_redirects=True)
        print(resp.status_code)

        open(file_path, "wb").write(resp.content)


        with ZipFile(file_path, 'r') as zipObject:
            zipObject.extractall(path="temp")


    except Exception as err:
        logging.error(err)
        sys.exit(-1)
        



def read_movies_csv(dataset_folder) -> list[Movie]:
    csv_movies_path =  f"{dataset_folder}/movies.csv"

    movies = []


    with open(csv_movies_path, "r") as movies_csv:
        csvreader = csv.reader(movies_csv)

        for row in csvreader:
            genres = row[-1].split("|")
            index_year =  row[1].find("(") 

            year =  row[1][index_year+1:-1]

            title = row[1][:index_year]

            movie_id = row[0]


            movie = Movie(movie_id, title, year, genres)


            movies.append(movie)


    return movies
        



if __name__ == "__main__":
    print("Load Movies Dataset to Elastic Search")

    elastic_url = "http://localhost:9200"

    filepath = "temp/ml-latest-small"

    download_and_unzip_dataset()
    
    movies = read_movies_csv(filepath)


    elastic_client = connect_elastic(elastic_url)



    try:
        elastic_client.indices.create(index="movies") 
    except Exception as err:
        logging.error(err)


        


    generator_movies = gen_movie_docs(movies, "movies")

    logging.info("Inserindo os filmes no Elastic Search")

    print(bulk(elastic_client, generator_movies))

    logging.info("Filmes inseridos com sucesso!!!")








        




    






