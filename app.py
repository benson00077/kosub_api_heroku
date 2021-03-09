import os
from flask import Flask, request, jsonify
import psycopg2 
import psycopg2.extras # for row read in db teturn as dictionary like values, instaed of default list of tuple
import ast, re
from time import strftime, localtime
from helper import prettify, dict_factory
from flask_cors import cross_origin
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['JSON_AS_ASCII'] = False
# setting for db in Heroku, using psycopg2 to connect DATABSE_URL
# in LocalHost: $ export DATABASE_URL="postgresql:///kosub_subtitles", which is invoke in .env file with autoenv module in localhost
DATABASE_URL = os.environ['DATABASE_URL']


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Kosub RESTful API</h1>
<p>A prototype API for Kosub query.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

#get /sub/query/ko?word=사랑하다 
#data {"en":[...], "ko":[...], "zh":[...], "id":[...]}
@app.route('/sub/query/ko', methods=['GET'])
@cross_origin()
def api_word_ko():
    query_parameters = request.args
    
    # analyze word
    word = query_parameters.get('word')
    if not word:
        return page_not_found(404)
    
    if word[-2:] == '하다':
        stem = word[:-2]
        stem_Regex = re.compile(stem + r"/NNG*")   # 之後查POS用，例如[['사랑/NNG', '하/XSV', '는/ETD'], ['이/NNG', '들/XSN', '의/JKG']]]
    elif word[-3:] == '스럽다':
        stem = word[:-3]
        stem_Regex = re.compile(stem + r"/NNG")   # 之後查POS用，例如　자연/NNG | 스럽/XSA | 죠/EFN |
    elif word[-1:] == '다':
        stem = word[:-1]
        stem_Regex = re.compile(stem + r"/V.*")    # 之後查POS用，例如　이러/VV | 고/ECE | 자/VV  排除남자, 자신....
    else:
        return "<h1>404</h1><p>The resource could not be found.</p>", 404

    # init db
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    query = '''SELECT kopos.id, pos, tag, morphs,
                      kosentence.sentence AS stn_ko,
                      kosentence_en.sentence AS stn_en,
                      kosentence_zh.sentence AS stn_zh
                FROM "kopos"
                JOIN kosentence ON kopos.id = kosentence.id
                JOIN kosentence_en ON kopos.id = kosentence_en.id
                JOIN kosentence_zh ON kopos.id = kosentence_zh.id'''
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute(query)
    rows2 = cur.fetchall()

    # Settings for data UPDATE / READ
    match = {"id":[], "ko":[], "en":[], "zh":[] }

    # Mapping match result
    for row in rows2:                             # eg. rows['pos'] as string, like "[['도깨비/NNG', '가/JKC'], ['되/VV', 'ㄴ단다/EFN']]"
        if stem_Regex.search(row['pos']):            
            # append Ko matched result to list
            stn_ko = row['stn_ko']
            stn_ko = prettify(stn_ko)
            match["ko"].append(stn_ko)
            # append eng matched result to list
            stn_en = row['stn_en']
            stn_en = prettify(stn_en)
            match["en"].append(stn_en)
            # append zh matched result to list
            stn_zh = row['stn_zh']
            stn_zh = prettify(stn_zh)
            match["zh"].append(stn_zh)
            # append matched sentence id to list
            match["id"].append(row['id'])

    if conn:
        cur.close()
        conn.close()

    return match

#get /sub/query/zh?word=叔叔
#data {"en":[...], "ko":[...], "zh":[...], "id":[...]}
@app.route('/sub/query/zh', methods=['GET'])
@cross_origin()
def api_word_zh():
    query_parameters = request.args
    
    # analyze word
    word = query_parameters.get('word')
    if not word:
        return page_not_found(404)

    # init db
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    query = '''SELECT kosentence.id,
                      kosentence.sentence AS stn_ko,
                      kosentence_en.sentence AS stn_en,
                      kosentence_zh.sentence AS stn_zh
                FROM "kosentence"
                JOIN kosentence_en ON kosentence.id = kosentence_en.id
                JOIN kosentence_zh ON kosentence.id = kosentence_zh.id'''
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute(query)
    rows2 = cur.fetchall()

    # Settings for data UPDATE / READ
    match = {"id":[], "ko":[], "en":[], "zh":[] }

    # Mapping match result
    for row in rows2:
        row_literal = ast.literal_eval(row['stn_zh'])
        for item in row_literal:                     # row_literal could be: ['叔叔\n', '\n']
            if word in item:
                # append Ko matched result to list
                stn_ko = row['stn_ko']
                stn_ko = prettify(stn_ko)
                match["ko"].append(stn_ko)
                # append eng matched result to list
                stn_en = row['stn_en']
                stn_en = prettify(stn_en)
                match["en"].append(stn_en)
                # append zh matched result to list
                stn_zh = row['stn_zh']
                stn_zh = prettify(stn_zh)
                match["zh"].append(stn_zh)
                # append matched sentence id to list
                match["id"].append(row['id'])

    if conn:
        cur.close()
        conn.close()

    return match

#get /sub/query/en?word=goblin
#data {"en":[...], "ko":[...], "zh":[...], "id":[...]}
@app.route('/sub/query/en', methods=['GET'])
@cross_origin()
def api_word_en():
    query_parameters = request.args
    
    # analyze word
    word = query_parameters.get('word')
    if not word:
        return page_not_found(404)

    # init db
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    query = '''SELECT kosentence.id,
                      kosentence.sentence AS stn_ko,
                      kosentence_en.sentence AS stn_en,
                      kosentence_zh.sentence AS stn_zh
                FROM "kosentence"
                JOIN kosentence_en ON kosentence.id = kosentence_en.id
                JOIN kosentence_zh ON kosentence.id = kosentence_zh.id'''
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute(query)
    rows2 = cur.fetchall()

    # Settings for data UPDATE / READ
    match = {"id":[], "ko":[], "en":[], "zh":[] }

    # Mapping match result
    for row in rows2:
        row_literal = ast.literal_eval(row['stn_en'])
        for item in row_literal:
            if word in item:           
                    # append Ko matched result to list
                    stn_ko = row['stn_ko']
                    stn_ko = prettify(stn_ko)
                    match["ko"].append(stn_ko)
                    # append eng matched result to list
                    stn_en = row['stn_en']
                    stn_en = prettify(stn_en)
                    match["en"].append(stn_en)
                    # append zh matched result to list
                    stn_zh = row['stn_zh']
                    stn_zh = prettify(stn_zh)
                    match["zh"].append(stn_zh)
                    # append matched sentence id to list
                    match["id"].append(row['id'])

    if conn:
        conn.close()

    return match

# get: /sub/search/all?id=11005532537&contextrange=5000
# data {..., "11005532537": {"ko":"...", "en":"...", "zh":"..."}}
@app.route('/sub/search/all', methods=['GET'])
@cross_origin()
def api_kosentence_all():
    query_parameters = request.args

    id = query_parameters.get('id')
    contextRange = query_parameters.get('contextrange')

    query = '''SELECT kosentence.id AS id,
                      kosentence.sentence AS stn_ko,
                      kosentence_en.sentence AS stn_en,
                      kosentence_zh.sentence AS stn_zh
                FROM "kosentence"
                JOIN kosentence_en ON kosentence.id = kosentence_en.id
                JOIN kosentence_zh ON kosentence.id = kosentence_zh.id
                WHERE '''

    to_filter = []

    if contextRange:
        sec = int(contextRange)
        query+= f' kosentence.id BETWEEN {int(id)-sec} and {int(id)+sec};'
    elif id:
        query += ' kosentence.id=?;'
        to_filter.append(id)
    else:
        return page_not_found(404)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute(query, to_filter) #### maybe invalid in postgreSQL
    results = cur.fetchall()
    
    match = {"id":[], "ko":[], "en":[], "zh":[] }
    for result in results:
        result['stn_ko'] = prettify(result['stn_ko']) # data: [..., {"id":111, "sentence": "(덕화) 안 되는 거야"}]
        result['stn_zh'] = prettify(result['stn_zh'])
        result['stn_en'] = prettify(result['stn_en'])
        match["id"].append(result['id'])
        match["ko"].append(result['stn_ko'])
        match["en"].append(result['stn_en'])
        match["zh"].append(result['stn_zh'])

    if conn:
        conn.close()
    # return jsonify(results)
    return match


#get  /sub/sentencebook?id=1
#  data 
#post /sub/sentencebook
#  data [..., {"id":1, "sentence_id":11005532537, "query":"도깨비"}]
@app.route('/sub/sentencebook', methods=['GET','POST'])
@cross_origin()
def api_push_sentencebook():
    if request.method == "POST":
        request_datas = request.get_json()
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        # UPDATE sentencebook table
        conn = pyscopg2.cnnect(DATABASE_URL, sslmode='require')
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        for data in request_datas:
            print(data)
            # cur.execute('''INSERT INTO sentencebook (id,sentence_id,time,query)
            #                     VALUES (:id, :sentence_id, :time, :query)''',
            #                     {'id': data['id'],
            #                     'sentence_id': data['sentence_id'],
            #                     'time': time,
            #                     'query': data['query']})
            cur.execute('''INSERT INTO "sentencebook" (id,sentence_id,time,query)
                                VALUES (%s, %s, %s, %s)''',
                                (data['id'], data['sentence_id'], time, data['query']))

        if conn:
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"data": data, "isAddedToSentencebook": True})

        return jsonify({"isAddedToSentencebook": False})

    if request.method == "GET":
        
        id_parameters = request.args
        if not id_parameters:
            return page_not_found(404)
        user_id = id_parameters.get('id')

        # READ sentencebook table
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # Settings for data READ
        match_id = []
        match_ko = []
        match_en = []
        match_zh = []

        # READ combined sentnece table & kosentence table
        # rows = cur.execute('''SELECT sentencebook.id, sentence_id, time, query,
        #                             kosentence.sentence AS stn_ko,
        #                             kosentence_en.sentence AS stn_en,
        #                             kosentence_zh.sentence AS stn_zh
        #                     FROM sentencebook
        #                     JOIN kosentence ON sentence_id = kosentence.id
        #                     JOIN kosentence_en ON sentence_id = kosentence_en.id
        #                     JOIN kosentence_zh ON sentence_id = kosentence_zh.id
        #                     WHERE sentencebook.id = :id
        #                     ORDER BY time''',
        #                     {'id': user_id})
        cur.execute('''SELECT sentencebook.id, sentence_id, time, query,
                                    kosentence.sentence AS stn_ko,
                                    kosentence_en.sentence AS stn_en,
                                    kosentence_zh.sentence AS stn_zh
                            FROM "sentencebook"
                            JOIN kosentence ON sentence_id = kosentence.id
                            JOIN kosentence_en ON sentence_id = kosentence_en.id
                            JOIN kosentence_zh ON sentence_id = kosentence_zh.id
                            WHERE sentencebook.id = %s
                            ORDER BY time''',
                            (user_id))
        rows = cur.fetchall()

        print(f"----------- Accessing user:{user_id}'s Sentence Book")
        for row in rows:
            match_id.append(row['sentence_id'])
            match_ko.append(prettify(row['stn_ko']))
            match_en.append(prettify(row['stn_en']))
            match_zh.append(prettify(row['stn_zh']))

        if conn:
            cur.close()
            conn.close()
        
        match = {"id":match_id, "ko":match_ko, "en":match_en, "zh":match_zh}
        return match


#post /sub/sentencebook/del
#  data [..., {"id":1, "sentence_id":11005532537, "query":"도깨비"}]
@app.route('/sub/sentencebook/del', methods=['POST'])
@cross_origin()
def api_del_sentencebook():
    if request.method == "POST":
        request_datas = request.get_json()
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        # DEL sentencebook table
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        for data in request_datas:
            print(data)
            # cur.execute('''DELETE FROM sentencebook
            #                     WHERE (id = :id AND sentence_id= :sentence_id)''',
            #                     {'id': data['id'],
            #                     'sentence_id': data['sentence_id']})
            cur.execute('''DELETE FROM "sentencebook"
                                WHERE (id = %s AND sentence_id= %s)''',
                                (data['id'], data['sentence_id']))

        if conn:
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"data": data, "isDeletedFromSentencebook": True})

        return jsonify({"isDeletedFromSentencebook": False})



#post /sub/login
#data {"user": "...", "pass": "..."}
@app.route("/sub/login", methods=["POST"])
@cross_origin()
def login():

    request_datas = request.get_json()

    # UPDATE login table
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute('''SELECT * FROM "users" WHERE username = %s''',
                        (request_datas["user"]))
    rows = cur.fetchall()

    userId = ""
    for row in rows:
        userId = row["id"]
        print(row) # {'id': 1, 'username': 'test1234', 'hash': '.....'}
        print(f"user: {request_datas['user']} (id: {userId}) just logged in")
        if not check_password_hash(row["hash"], request_datas["pass"]):
            # invalid username and/or password
            return {'isLoggedIn': False}
        
        if conn:
            conn.close()
        return {'userID': userId, 'isLoggedIn': True}

    # "nvalid username and/or password
    return {'isLoggedIn': False} 

#post /sub/register
#data {"user": "...", "pass": "..."}
@app.route("/sub/register", methods=["POST"])
@cross_origin()
def register():

    request_datas = request.get_json()

    # UPDATE register table
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute('''INSERT INTO users (username,hash)
                          VALUES (%s, %s)''',
                          (request_datas["user"], 
                          generate_password_hash(request_datas["pass"])))                      
    
    conn.commit()

    print(f"user: {request_datas['user']} just registered")

    if conn:
        cur.close()
        conn.close()

    return f"user: {request_datas['user']} just registered"

if __name__ == "__main__":
    app.run()