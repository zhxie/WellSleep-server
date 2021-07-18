import constant
import db
from flask import Flask, request

app = Flask(__name__)


def is_id_valid(content):
    try:
        if content is None:
            return False

        if content['id'] is None:
            return False
        id = int(content['id'])
        if id < 0 or id > 999999999:
            return False

        return True
    except:
        return False


def is_nickname_valid(content):
    try:
        if content is None:
            return False

        if content['nickname'] is None:
            return False
        if len(str(content['nickname'])) <= 0:
            return False

        return True
    except:
        return False


def is_type_valid(content):
    try:
        if content is None:
            return False

        if content['type'] is None:
            return False
        type = int(content['type'])
        if type != constant.TYPE_CHECK_IN and type != constant.TYPE_CHECK_OUT:
            return False

        return True
    except:
        return False


def is_followee_valid(content):
    try:
        if content is None:
            return False

        if content['followee'] is None:
            return False
        followee = int(content['followee'])
        if followee < 0 or followee > 999999999:
            return False

        return True
    except:
        return False


def is_to_valid(content):
    try:
        if content is None:
            return False

        if content['to'] is None:
            return False
        to = int(content['to'])
        if to < 0:
            return False

        return True
    except:
        return False


def is_limit_valid(content):
    try:
        if content is None:
            return False

        if content['limit'] is None:
            return False
        limit = int(content['limit'])
        if limit < 1:
            return False

        return True
    except:
        return False


@app.route('/register', methods=['POST'])
def register():
    content = request.get_json()
    if is_nickname_valid(content):
        id = db.register(str(content['nickname']))
        if id < 0:
            return {
                'status': id,
            }
        else:
            return {
                'status': constant.SUCCESS,
                'id': id
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/update_profile', methods=['POST'])
def update_profile():
    content = request.get_json()
    if is_id_valid(content) and is_nickname_valid(content):
        return {
            'status': db.update_profile(content['id'], content['nickname'])
        }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/check', methods=['POST'])
def check():
    content = request.get_json()
    if is_id_valid(content) and is_type_valid(content):
        ts = db.check(content['id'], content['type'],
                      content['weather'] if 'weather' in content else None)
        if ts < 0:
            return {
                'status': ts
            }
        else:
            return {
                'status': constant.SUCCESS,
                'time': ts
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/follow', methods=['POST'])
def follow():
    content = request.get_json()
    if is_id_valid(content) and is_followee_valid(content):
        id = content['id']
        followee = content['followee']
        if id != followee:
            return {
                'status': db.follow(id, followee)
            }
        else:
            return {
                'status': constant.ERR_FOLLOWEE_IS_USER
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/unfollow', methods=['POST'])
def unfollow():
    content = request.get_json()
    if is_id_valid(content) and is_followee_valid(content):
        id = content['id']
        followee = content['followee']
        if id != followee:
            return {
                'status': db.unfollow(id, followee)
            }
        else:
            return {
                'status': constant.ERR_FOLLOWEE_IS_USER
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/user', methods=['GET'])
def user():
    content = request.args
    if is_id_valid(content):
        r = db.user(content['id'])
        if type(r) == int:
            return {
                'status': r
            }
        else:
            return {
                'status': constant.SUCCESS,
                'id': r['id'],
                'nickname': r['nickname'],
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/activities', methods=['GET'])
def activities():
    content = request.args
    if is_id_valid(content) and is_to_valid(content) and is_limit_valid(content):
        r = db.activities(content['id'], content['to'], content['limit'])
        if type(r) == int:
            return {
                'status': r
            }
        else:
            return {
                'status': constant.SUCCESS,
                'activities': r['activities']
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/followers', methods=['GET'])
def followers():
    content = request.args
    if is_id_valid(content):
        r = db.followers(content['id'])
        if type(r) == int:
            return {
                'status': r
            }
        else:
            return {
                'status': constant.SUCCESS,
                'followers': r['followers']
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }


@app.route('/timeline', methods=['GET'])
def timeline():
    content = request.args
    if is_id_valid(content) and is_to_valid(content) and is_limit_valid(content):
        r = db.timeline(content['id'], content['to'], content['limit'])
        if type(r) == int:
            return {
                'status': r
            }
        else:
            return {
                'status': constant.SUCCESS,
                'timeline': r['timeline'],
                'id': r['id'],
                'nickname': r['nickname'],
                'followers': r['followers']
            }
    else:
        return {
            'status': constant.ERR_INVALID_PARAM
        }
