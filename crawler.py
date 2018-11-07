import requests
import ujson


def get_paper_ratings(paper_id):
    cookies = {
        '_ga': 'GA1.2.476467575.1538141684',
        '_gid': 'GA1.2.2099116047.1541498115',
        '_gat_gtag_UA_108703919_1': '1',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,en-US;q=0.9,fa;q=0.8,de;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://openreview.net/forum?id=' + paper_id,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('forum', paper_id),
        ('trash', 'true'),
        ('details', 'replyCount,writable,revisions,original,overwriting,tags'),
    )

    ratings = []
    response = requests.get('https://openreview.net/notes', headers=headers, params=params, cookies=cookies)
    response = response.json()
    for note in response['notes']:
        if 'rating' in note['content']:
            ratings.append(note['content']['rating'])
    return ratings


def get_paper_list(offset):
    cookies = {
        '_ga': 'GA1.2.476467575.1538141684',
        '_gid': 'GA1.2.2099116047.1541498115',
        '_gat_gtag_UA_108703919_1': '1',
    }

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,en-US;q=0.9,fa;q=0.8,de;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://openreview.net/group?id=ICLR.cc/2019/Conference',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    params = (
        ('invitation', 'ICLR.cc/2019/Conference/-/Blind_Submission'),
        ('offset', offset),
        ('details', 'replyCount,tags'),
        ('limit', '50'),
    )

    response = requests.get('https://openreview.net/notes', headers=headers, params=params, cookies=cookies)

    response = response.json()
    return response


paper_ratings = {}
offset = 0
try:
    while True:
        response = get_paper_list(offset)
        count = response['count']
        for note in response['notes']:
            paper_ratings[note['id']] = get_paper_ratings(note['id'])
        offset += len(response['notes'])
        if offset >= count:
            break
        print(offset)
        with open('t.json', 'w') as f:
            ujson.dump(paper_ratings, f)
except:
    pass

with open('iclr2019', 'w') as f:
    ujson.dump(paper_ratings, f)
