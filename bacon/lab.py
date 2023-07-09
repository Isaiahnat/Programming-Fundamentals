"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    processed_data = {}
    for i in raw_data:
        if (i[2], 1) not in processed_data:
            processed_data[(i[2], 1)] = [i[0], i[1]]
        else:
            processed_data[(i[2], 1)].append(i[0])
            processed_data[(i[2], 1)].append(i[1])

    for i in raw_data:
        if i[0] != i[1]:
            if i[0] in processed_data:
                if i[1] not in processed_data[i[0]]:
                    processed_data[i[0]].add(i[1])
            else:
                processed_data[i[0]] = {i[1]}

            if i[1] in processed_data:
                if i[0] not in processed_data[i[1]]:
                    processed_data[i[1]].add(i[0])
            else:
                processed_data[i[1]] = {i[0]}

    return processed_data


def acted_together(transformed_data, actor_id_1, actor_id_2):
    if actor_id_1 == actor_id_2 or actor_id_2 in transformed_data[actor_id_1]:
        return True
    else:
        return False


def actors_with_bacon_number(transformed_data, n):
    result = {4724}
    visited = set()
    for _ in range(n):
        temp = set()
        visited = visited.union(result)
        for i in result:
            temp = temp.union(transformed_data[i])
        result = temp
        result = result - visited
        if len(result) == 0:
            break
    return result


def idset_to_name(namepickle, idnumset):
    
    out = set()
    for i in namepickle:
        if namepickle[i] in idnumset:
            out.add(i)
    return out
    
def idlist_to_name(namepickle, idlist):
    out = []
    for i in idlist:
        out.append(id_to_name(namepickle, i))
    return out


def id_to_name(namepickle, id):
    for i in namepickle:
        if namepickle[i] == id:
            return i


def bacon_path(transformed_data, actor_id):
    return bfs(transformed_data, 4724, actor_id)


def construct_path(actor_id_1, actor_id_2, paths):
    out = [actor_id_2]
    current = actor_id_2
    while current != actor_id_1:
        out.append(paths[current])
        current = paths[current]
    out.reverse()
    return out


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    return bfs(transformed_data, actor_id_1, actor_id_2)

def bfs(transformed_data, actor_id_1, actor_id_2):
    paths = {}
    visited = set()
    que = [actor_id_1]
    if actor_id_1 == actor_id_2:
        return [actor_id_1]
    while que:
        for i in transformed_data[que[0]]:
            if i not in visited:
                paths[i] = que[0]
                visited.add(i)
                que.append(i)
        if actor_id_2 in visited:
            break
        que.pop(0)
    if len(que) == 0:
        return None
    return construct_path(actor_id_1, actor_id_2, paths)

def actor_path(transformed_data, actor_id_1, goal_test_function):
    paths = {}
    visited = set()
    que = [actor_id_1]
    endid = None
    if goal_test_function(actor_id_1):
        return [actor_id_1]
    while que:
        for i in transformed_data[que[0]]:
            if i not in visited:
                paths[i] = que[0]
                visited.add(i)
                que.append(i)
            if goal_test_function(i):
                endid = i
                break
        if endid is not None:
            break
        que.pop(0)
    if len(que) == 0:
        return None
    return construct_path(actor_id_1, endid, paths)
    


def is_in_film(movieid, transformed_data):
    def func(actorid):
        if actorid in transformed_data[(movieid, 1)]:
            return True
        else:
            return False
    return func


def actors_connecting_films(transformed_data, film1, film2):
    paths = None
    for i in transformed_data[(film1, 1)]:
        func = is_in_film(film2, transformed_data)
        temp=actor_path(transformed_data, i, func)
        if paths is None or temp is None:
            paths=temp
        elif len(temp)<len(paths):
            paths = temp
    return paths


def shape_movie_data(raw_data):
    out = {}
    for i in raw_data:
        out[(i[0], i[1])] = i[2]
    return out


def id_to_movie(moviedb, id):
    for i in moviedb:
        if moviedb[i] == id:
            return i


def actor_to_movie_path(movie_transformed_data, moviedb, path):
    out = []
    for i in range(1, len(path)):
        if (path[i - 1], path[i]) in movie_transformed_data:
            out.append(
                id_to_movie(moviedb, movie_transformed_data[(path[i - 1], path[i])])
            )
        elif (path[i], path[i - 1]) in movie_transformed_data:
            out.append(
                id_to_movie(moviedb, movie_transformed_data[(path[i], path[i - 1])])
            )
    return out


if __name__ == "__main__":
    # with open("resources/tiny.pickle", "rb") as x:
    #         tinydb = pickle.load(x)
    #
    # with open("resources/small.pickle", "rb") as f:
    #      smalldb = pickle.load(f)
    # print(smalldb)
    # test = transform_data(smalldb)
    # print(test)
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # for i in smalldb:
    #     if smalldb[i]==25663:
    #         print(i)
    # data = transform_data(smalldb)
    # with open ("resources/names.pickle", "rb") as f:
    #     names = pickle.load(f)
    # var = acted_together(data,names["Amanda Tilson"],names["Elisabeth Depardieu"])
    # var = acted_together(data,names["Stig Olin"],names["Jan Malmsjo"])
    # print(var)
    # with open("resources/tiny.pickle", "rb") as f:
    #     tinydb = pickle.load(f)
    # with open ("resources/large.pickle", "rb") as f:
    #     largedb = pickle.load(f)
    # largedb = transform_data(largedb)
    # actorset = actors_with_bacon_number(largedb, 6)
    # print(actorset)
    # actors = {1367972, 1338716, 1345461, 1345462}
    # print(idset_to_name(names, actors))
    # tinydb = transform_data(tinydb)
    # print(bacon_path(tinydb, 1640))
    # answer = bacon_path(largedb, names["Serigne Seck"])
    # for i in range(len(answer)):
    #     answer[i] = id_to_name(names,answer[i])
    # print(answer)
    # print(tinydb)
    # with open ("resources/movies.pickle", "rb") as f:
    #     movies = pickle.load(f)
    # print(movies)
    # id1 = names["Gunnar Teuber"]
    # id2 = names["Hannah Pilkes"]
    # actorlist = actor_to_actor_path(largedb,id1,id2)
    # actorlist = idlist_to_name(names,actorlist)
    # print(actorlist)
    # transformed = transform_data(largedb)
    # shapedmovies = shape_movie_data(largedb)
    # id1 = names["Willie Adams"]
    # id2 = names["Sven Batinic"]
    # path = actor_to_actor_path(transformed, id1, id2)
    # # print(actor_to_movie_path(shapedmovies,movies,path))
    # print(actors_connecting_films(transformed, 142416, 44521))
    pass
