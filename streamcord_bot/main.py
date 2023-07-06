# -*- coding = utf-8 -*-

# @Project : PyCharm
# @File    : main.py
# @Author  : yh0916.shi
# @E-mail  : yh0916.shi.w@outlook.com
# @Time    : 2023/7/6下午1:58


import os
import discord
import time
import datetime
from live_requests import live_request
from discord.ext import tasks
from dotenv import load_dotenv

# 创建Discord客户端，若需要使用到代理，则添加一个proxy='代理地址及端口'
client = discord.Client(intents=discord.Intents.default())

# 设定直播监测时间段
start_time = datetime.time(hour=16, minute=0, second=0)
end_time = datetime.time(hour=23, minute=0, second=0)
tz = datetime.timezone(datetime.timedelta(hours=8))

# 设置监测直播间号，设置全局变量及读取机器人key
room_id = 'target room'    # 直播房间号
time_clock = 0             # 全局计数器
load_dotenv('TOKEN.env')   # 获取discord机器人key
channel_id = int()         # 要输出信息的频道id

# 运行客户端
def run_bot():
    client.run(os.environ.get('TOKEN'))


# 关闭客户端
async def close_bot():
    await client.close()


# 设置通知函数，循环间隔时长为1min
@tasks.loop(minutes=1)
async def notification():
    # 引入全局变量计数器
    global time_clock, room_id, channel_id
    current_time = datetime.datetime.now(tz).time()
    if start_time <= current_time <= end_time:
        # 设定检查直播状态
        rm_id, flag, data = live_request(room_id)
        # while (flag != 1):
        #   rm_id, flag, data = live_request(room_id)
        #   print('not yet')
        #   await time.sleep(60)

        # 当直播状态为直播中(live_status = 1)时
        if flag == 1:
            # 获取直播信息同时设置discord内嵌信息
            # 直播间标题
            live_title = data['title']
            # 直播状态简介，可以写一些自己想写的内容介绍，例：
            live_status = "xxx has gone live on bilibili"
            # 直播间观众人数
            viewer_count = int(data['online'])
            # 获取直播间封面
            thumbnail_url = data['user_cover']

            # 创建嵌入式消息对象
            embed = discord.Embed(title=live_title,
                                  description=live_status,
                                  color=discord.Color.green())
            embed.add_field(name='Game', value='Overwatch2')
            embed.add_field(name='Viewers', value=viewer_count)
            # 添加一个直达直播间的超链接
            embed.add_field(name='Watch now',
                            value='[Click here](https://live.bilibili.com/%d)' %
                                  rm_id)
            # embed.set_thumbnail(url=thumbnail_url)
            embed.set_image(url=thumbnail_url)

            # 发送嵌入式消息到指定的频道
            # 将机器人邀请进服务器后，在想要发送消息的服务器频道中复制频道id
            channel = client.get_channel(channel_id)  # 数字格式不用加引号
            await channel.send(embed=embed)
            # print('Done')  # debug 在终端中打印机器人运行结果
            # 通知成功后关闭通知函数
            notification.stop()
            # 等待3秒
            time.sleep(3)
            # 关闭机器人
            await close_bot()

        else:
            # 非直播状态时，每5分钟打印一次当前状态
            # 在终端打印
            # print('not yet')
            time_clock = time_clock + 1
            if time_clock == 5:
                time_clock = 0
                channel = client.get_channel(channel_id)
                await channel.send('not yet')

    # 当脚本运行时晚于直播通知监测时间段，直接输出状态并关闭机器人
    elif current_time > end_time:
        channel = client.get_channel(channel_id)
        await channel.send("It's late")
        notification.stop()
        time.sleep(3)
        await close_bot()

    # 当脚本运行早于直播通知监测时段，打印当前状态
    else:
        time_clock = time_clock + 1
        if time_clock == 5:
            time_clock = 0
            channel = client.get_channel(channel_id)
            await channel.send('too early')
            # print('not right time')


# 判断机器人运行状态
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    notification.start()


# 运行Discord客户端
if __name__ == '__main__':
    run_bot()

