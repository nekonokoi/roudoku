# coding:utf-8
import falcon
from chat_function import chat_main
import json
import requests
import os

"""
STATIC
"""

with open("setting.json","rb") as f:
    setting = json.load(f)

LINE_ENDPOINT = "https://trialbot-api.line.me"
HEADERS = {
    'Content-Type':'application/json; charset=UTF-8',
    "X-Line-ChannelID":setting["channelID"],
    "X-Line-ChannelSecret":setting["channelSecret"],
    "X-Line-Trusted-User-With-ACL":setting["ACL"]
}
TO_CHANNEL = "1383378250"
EVENT_TYPE = "138311608800106203"
PROXIES = {
    'http':os.environ.get('FIXIE_URL', ''),
    'https':os.environ.get('FIXIE_URL', '')
}

class BotResource(object):
    def __init__(self):
        pass

    #callback and responce
    def on_post(self,req,resp):
        """
        call this when user acts on Lines Apps
        and this-func callbacks other0func by req-type
        """
        body = req.stream.read()
        param = json.loads(body.decode("utf-8"))
        # wyh list?
        print param
        to,res_content= dispatch(param["result"][0])
        print res_content
        print raise_event(to,res_content)
        resp.body = json.dumps('OK')

def raise_event(to,content,to_channel=TO_CHANNEL,event_type=EVENT_TYPE):
    """
    send text,pic,and others
    """

    data = json.dumps({
        "to":to,
        "toChannel":to_channel,
        "eventType":event_type,
        "content":content
    })

    res = requests.post(
        LINE_ENDPOINT + "/v1/events",
        data=data,
        headers=HEADERS,
        proxies=PROXIES)
    return res


def dispatch(req):
    """
    call from bot_app class
    and routing by data

    >>> to,text = dispatch({"eventType":"138311609000106303","content":{"from":"test_from"}})
    >>> to
    ['test_from']
    >>> text['contentType']
    1
    >>> text['toType']
    1

    >>> to,text = dispatch({"eventType":"138311609100106403","from":"test_from"})
    >>> to
    ['test_from']
    >>> text['contentType']
    1
    >>> text['toType']
    1
    """

    # require friend
    if req["eventType"] == "138311609100106403":
        text = chat_main("test")
        to = [req["from"]]

        data = make_text_post(text)
        return to,data

    # get chat
    elif req["eventType"] == "138311609000106303":
        text = chat_main("test")
        to = [req["content"]["from"]]

        data = make_text_post(text)
        return to,data


# make_contents_functions
def make_text_post(text):
    """
    make json for response
    this is for text

    >>> make_text_post('test')
    {'text': 'test', 'contentType': 1, 'toType': 1}
    """
    # @TODO:typeError

    data = {
        "contentType":1,
        "toType":1,
        "text":text
    }

    return data

api = falcon.API()
api.add_route('/callback',BotResource())

if __name__=="__main__":
    import doctest
    doctest.testmod()
