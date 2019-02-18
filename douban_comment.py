import requests
import re
from lxml import etree
import time
import xlwt


#爬取电影标题及评论节点
def got_data_by_ID(conda):
    data = []
    response = requests.get('https://movie.douban.com/subject/{}/comments?status=P'.format(conda))
    # print(response.text)
    res_xpath = etree.HTML(response.text)
    #提取标题
    print(res_xpath.xpath('//*[@id="content"]/h1/text()')[0])
    title = res_xpath.xpath('//*[@id="content"]/h1/text()')[0]
    #提取所有的评论节点nodes，因为需要二次提取
    nodes = res_xpath.xpath('//*[@id="comments"]/div[@class="comment-item"]')
    #二次提取
    for node in nodes:
        name = node.xpath('./div[1]/a/@title')[0]
        comment = node.xpath('./div[2]/p/span/text()')[0]
        lavel = node.xpath('./div[2]/h3/span[2]/span[2]/@title')[0]
        print('名字：',name)
        print('影评内容：',comment)
        print('个人评分：', lavel)
        data.append([name,comment,lavel])
    sava_data(title,data)
#写入数据到Excel中
def sava_data(title,data):
    #创建一个新的表格
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    #创建一个sheet
    sheet = book.add_sheet('豆瓣短评',cell_overwrite_ok=True)

    col = ('名字','影评内容','个人评分')
    #写入第一列   表头
    for i in range(0,3):
        sheet.write(0,i,col[i])#列名
    #写入内容
    for i in range(0,20):#前20条短评

        for j in range(0,3):
            sheet.write(i + 1,j,data[i][j])#数据
    book.save(title+".xls")#保存

#爬取所有的电影编号
def get_code():
    #总共为10页
    for page in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(page*25)
        response = requests.get(url)
        for movie_code in set(re.findall(r'https://movie.douban.com/subject/(\d+)/',response.text ,re.S)):#数据清洗
            time.sleep(3)
            got_data_by_ID(movie_code)

get_code()





