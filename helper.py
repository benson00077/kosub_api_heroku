import ast, re

# from r"['[타이어 마찰음]\n', '오직 도깨비 신부만이\n', '\n']"
# to [타이어 마찰음], 오직 도깨비 신부만
def prettify(raw_str):
    subtitle_list = ast.literal_eval(raw_str)
    processed_str = ''
    for subtitle in subtitle_list:
        subtitle = re.sub(r'\n', '', subtitle)
        processed_str += subtitle
    return processed_str


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d