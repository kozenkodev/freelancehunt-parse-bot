import re
import requests
import time
from bs4 import BeautifulSoup
from lxml import html
from aiogram import Bot, Dispatcher, executor, types
Orderd_list=[]
#class for parse and send data to channel
class ParserData(object):
    async def ParsePost(self, link):
            r = requests.post(url=link)
            tree = html.fromstring(r.content)
            data=f"{link}\n"
            date=tree.xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div[2]/div/div/div[2]/span")[0].text_content()
            price=tree.xpath("/html/body/div[1]/div[2]/div/div[2]/div/span[1]/span")
            if len(price)!=0:
                data=data+f"Цена: {price[0].text_content()}\n"
            for i in tree.xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/span/p"):
                if i.text_content().lower():
                 data=data+i.text_content()+"\n"
            await bot.send_message(chat_id="@your_channel",text=data)


    async def ParseLinks(self,link):
        LinkList = []
        r = requests.post(url=link)
        scrapper=BeautifulSoup(r.content,"html.parser")
        for item in scrapper.find_all('td',class_="left"):
            for sub_item in item.find_all('a',class_="bigger visitable"):
                LinkList.append(sub_item.get('href'))
                reg = re.compile('[^0-9]')
                dt = reg.sub('', sub_item.get('href'))
                if dt in Orderd_list:
                    pass
                else:
                    Orderd_list.append(dt)
                    await self.ParsePost(sub_item.get('href'))
             
bot = Bot(token="your bot token")
dp = Dispatcher(bot)
async def main():
    obt = ParserData()
    while True:
        await obt.ParseLinks("https://freelancehunt.ua/projects/skill/razrabotka-botov/180.html")
        time.sleep(200)
if __name__ == '__main__':
    executor.start(dp, main())
