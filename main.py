import json
import utils
from flask import Flask


SOURCE_DB = "netflix_hw_14.db"

app = Flask(__name__)

@app.route('/movie/<title>/')
def page_search_by_title(title):
    query_sql = utils.search_for_name(title)
    result_search_by_title = utils.connect_db(query_sql)

    result = {}
    for film in result_search_by_title:
        result = dict(film)

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        mimetype='application/json',
        status=200
    )


@app.route('/movie/<start_date>/to/<end_date>/')
def page_search_by_date(start_date, end_date):
    query_sql = utils.search_by_date(start_date, end_date)
    result_search_by_date = utils.connect_db(query_sql)

    result = []
    for film in result_search_by_date:
         result.append(dict(film))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        mimetype='application/json',
        status=200
        )


@app.route('/rating/<rating>/')
def page_search_by_rating(rating):
    query_sql = utils.search_by_rating(str(rating))
    result_search_by_rating = utils.connect_db(query_sql)

    result = []
    for film in result_search_by_rating:
        result.append(dict(film))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        mimetype='application/json',
        status=200
        )


@app.route('/genre/<genre>/')
def page_search_by_genre(genre):
    query_sql = utils.search_by_genre(genre)
    result_search_by_genre = utils.connect_db(query_sql)

    result = []
    for film in result_search_by_genre:
        result.append(dict(film))

    return app.response_class(
        json.dumps(result, ensure_ascii=False, indent=4),
        mimetype='application/json',
        status=200
    )


if __name__ == '__main__':
    print("Шаг 5")
    utils.search_actor('Rose McIver', 'Ben Lamb')
    utils.search_actor('Jack Black', 'Dustin Hoffman')
    print("\nШаг 6")
    print(utils.get_picture('Movie', 2020, 'Dramas'))

    app.run()



