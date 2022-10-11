import json
import sqlite3

SOURCE_DB = "netflix_hw_14.db"


def connect_db(query):
    with sqlite3.connect(SOURCE_DB) as con:
        con.row_factory = sqlite3.Row  # выгрузка построчно в виде словаря
        result = con.execute(query)
        executed_query = result.fetchall()
        return executed_query


def search_for_name(title_film):
    query = f"""SELECT title, country, release_year, listed_in as genre, description 
    from netflix n 
    where n.title = '{title_film}'
    order by release_year desc
    limit 1"""
    return query


def search_by_date(start_date, end_date):
    if start_date < end_date:
        query = f"""SELECT title, release_year 
            from netflix n 
            where release_year between {start_date} and {end_date}
            limit 100"""
    else:
        query = f"""SELECT title, release_year 
                    from netflix n 
                    where release_year between {end_date} and {start_date}
                    limit 100"""
    return query


def search_by_rating(rating):
    rating_list = {
        "children": ('G'),
        "family": ('G', 'PG', 'PG-13'),
        "adult": ('R', 'NC-17')
    }
    if rating == 'children':
        query = f"""SELECT n.title, n.rating, n.description from netflix n
                    where n.rating = 'G'"""
    else:
        query = f"""SELECT n.title, n.rating, n.description from netflix n
                    where n.rating in {rating_list.get(rating, ('G', 'R', 'NC-17'))}"""

    return query


def search_by_genre(genre):
    query = f"""
            SELECT n.title, n.description from netflix n
            where listed_in LIKE ('%{genre.title()}%')
            """
    return query


def search_actor(actor_name_one, actor_name_two):
    query = f"""
            SELECT n.title, n."cast", n.description from netflix n
            where n."cast" LIKE  ('%{actor_name_one}%') and n."cast" LIKE  ('%{actor_name_two}%')
            """
    actor_name_dict = {}
    result_search_actor = connect_db(query)
    for actor in result_search_actor:
        result = dict(actor)

        actor_names = set(result.get('cast').split(', ')) - set([actor_name_one, actor_name_two])

        for name in actor_names:
            actor_name_dict[name] = actor_name_dict.get(name, 0) + 1

    for key, value in actor_name_dict.items():
        if value > 2:
            print(key)


def get_picture(type_picture, release_year, genre):
    query = f"""SELECT 
                    n.show_id, 
                    n.title, 
                    n."type", 
                    n.director, 
                    n.release_year, 
                    n.rating, 
                    n.duration,
                    n.duration_type,
                    n.country,
                    n.listed_in,
                    n.description  
                from netflix n
                where n."type" = '{type_picture}' 
		        and n.release_year = {release_year} 
		        and n.listed_in like ('%{genre}%')
		        """

    result_get_picture = connect_db(query)

    results = []
    for result in result_get_picture:
        results.append(dict(result))
    return json.dumps(results, ensure_ascii=False, indent=4)
