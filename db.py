import constant
from datetime import datetime
import random
import sqlite3
import sys


def create_users_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (id         INTEGER PRIMARY KEY NOT NULL,
                 nickname   TEXT    NOT NULL)''')
    conn.commit()


def create_activities_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS activities
                (id         INTEGER PRIMARY KEY AUTOINCREMENT,
                 author     INTEGER NOT NULL,
                 type       INTEGER NOT NULL,
                 time       INTEGER NOT NULL,
                 weather    INTEGER)''')


def create_relation_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS relation
                (id         INTEGER NOT NULL,
                followee    INTEGER NOT NULL)''')


conn = sqlite3.connect('main.db')
cur = conn.cursor()
create_users_table()
create_activities_table()
create_relation_table()
conn.close()


def exist(cur, id):
    cur.execute('SELECT * FROM users WHERE id=' + str(id))

    return cur.fetchone() is not None


def followed(cur, id, followee):
    cur.execute('SELECT * FROM relation WHERE id=' +
                str(id) + ' AND followee=' + str(followee))

    return cur.fetchone() is not None


def register(nickname):
    while True:
        id = random.randint(0, 999999999)
        with sqlite3.connect('main.db') as conn:
            cur = conn.cursor()
            if not exist(cur, id):
                try:
                    cur.execute(
                        "INSERT INTO users VALUES (" + str(id) + ", '" + str(nickname) + "')")
                    conn.commit()

                    return id
                except:
                    return constant.ERR_INTERNAL_ERROR


def update_profile(id, nickname):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id):
            try:
                cur.execute("UPDATE users SET nickname='" +
                            nickname + "' WHERE id=" + str(id))
                conn.commit()

                return constant.SUCCESS
            except:
                return constant.ERR_INTERNAL_ERROR
        else:
            return constant.ERR_USER_NOT_EXIST


def check(id, type, weather):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id):
            try:
                ts = int(datetime.now().timestamp() * 1000)

                if weather is None:
                    cur.execute('INSERT INTO activities (author, type, time) VALUES(' +
                                str(id) + ', ' + str(type) + ', ' + str(ts) + ')')
                else:
                    cur.execute('INSERT INTO activities (author, type, time, weather) VALUES(' +
                                str(id) + ', ' + str(type) + ', ' + str(ts) + ', ' + str(weather) + ')')
                conn.commit()

                return ts
            except:
                return constant.ERR_INTERNAL_ERROR
        else:
            return constant.ERR_USER_NOT_EXIST


def follow(id, followee):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id) and exist(cur, followee):
            if followed(cur, id, followee) and followed(cur, followee, id):
                return constant.WARN_ALREADY_FOLLOWED
            else:
                try:
                    cur.execute('INSERT INTO relation VALUES(' +
                                str(id) + ', ' + str(followee) + ')')
                    cur.execute('INSERT INTO relation VALUES(' +
                                str(followee) + ', ' + str(id) + ')')
                    return constant.SUCCESS
                except:
                    return constant.ERR_INTERNAL_ERROR
        else:
            return constant.ERR_USER_NOT_EXIST


def unfollow(id, followee):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id) and exist(cur, followee):
            if followed(cur, id, followee) or followed(cur, id, followee):
                try:
                    cur.execute('DELETE FROM relation WHERE id=' +
                                str(id) + ' AND followee=' + str(followee))
                    cur.execute('DELETE FROM relation WHERE id=' +
                                str(followee) + ' AND followee=' + str(id))
                    return constant.SUCCESS
                except:
                    return constant.ERR_INTERNAL_ERROR
            else:
                return constant.WARN_NOT_FOLLOWED
        else:
            return constant.ERR_USER_NOT_EXIST


def user_internal(cur, id):
    return {
        'id': int(id),
        'nickname': cur.execute('SELECT nickname FROM users WHERE id=' + str(id)).fetchone()[0]
    }


def user(id):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id):
            return user_internal(cur, id)
        else:
            return constant.ERR_USER_NOT_EXIST


def activities_internal(cur, id, to, limit):
    t = int(to)
    if t == 0:
        t = sys.maxsize // 2

    ac = []
    for row in cur.execute('SELECT * FROM activities WHERE author=' +
                           str(id) + ' AND id<' + str(t) + ' ORDER BY id DESC LIMIT ' + str(limit)).fetchall():
        ac.append({'id': int(row[0]), 'type': int(
            row[2]), 'time': int(row[3]), 'weather': None if row[4] is None else int(row[4])})

    ac.sort(key=lambda x: x['time'], reverse=True)

    return {
        'activities': ac
    }


def activities(id, to, limit):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id):
            return activities_internal(cur, id, to, limit)
        else:
            return constant.ERR_USER_NOT_EXIST


def followers_internal(cur, id):
    s = set()
    for row in cur.execute('SELECT * FROM relation WHERE id=' + str(id)).fetchall():
        s.add(int(row[1]))
    for row in cur.execute('SELECT * FROM relation WHERE followee=' + str(id)).fetchall():
        s.add(int(row[0]))

    fs = []
    for f in s:
        fs.append({
            'id': f,
            'nickname': user_internal(cur, f)['nickname']
        })

    fs.sort(key=lambda x: x['nickname'])

    return {
        'followers': fs
    }


def followers(id):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id):
            return followers_internal(cur, id)
        else:
            return constant.ERR_USER_NOT_EXIST


def timeline(id, to, limit):
    with sqlite3.connect('main.db') as conn:
        cur = conn.cursor()
        if exist(cur, id):
            nn = user_internal(cur, id)['nickname']

            fs = followers_internal(cur, id)['followers']

            ac = []
            for f in fs:
                for a in activities_internal(cur, f['id'], to, limit)['activities']:
                    a['author'] = f['id']
                    ac.append(a)
            for a in activities_internal(cur, id, to, limit)['activities']:
                a['author'] = int(id)
                ac.append(a)

            ac.sort(key=lambda x: x['time'], reverse=True)

            return {
                'timeline': ac[:min(int(limit), len(ac))],
                'id': int(id),
                'nickname': nn,
                'followers': fs
            }
        else:
            return constant.ERR_USER_NOT_EXIST
