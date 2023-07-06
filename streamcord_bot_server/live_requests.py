import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
}

# bilibili-api: https://github.com/SocialSisterYi/bilibili-API-collect/
# url后加房间号
url = 'https://api.live.bilibili.com/room/v1/Room/get_info?room_id='


# 直播间信息获取函数，输入参数为房间号，返回房间号信息、直播状态和直播间信息
def live_request(room_id):
    request_url = url + str(room_id)
    request = requests.request(url=request_url, headers=header, method='GET')
    # 获取到的数据是json格式的，需要使用json解析
    data = request.json()
    # 返回房间号信息room_id,直播状态live_status,直播间信息data
    return room_id, data['data']['live_status'], data['data']


if __name__ == '__main__':
    room_id, live_status, live_info = live_request(room_id=1)
    print(live_info)
