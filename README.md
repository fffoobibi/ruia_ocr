# ruia_ocr

#### 介绍
一款ruia_ocr插件, 使用baidu-aip接口识别本地或远程图片

#### 软件架构
    依赖的库: baidu-aip, ruia
    运行环境: python 3.7, python 3.8, python 3.9

#### 安装教程

1.  python setup.py install

#### 使用说明
实现BaseOcrService

    from ruia import Item
    from ruia_ocr import (OcrField, BaiduOcrService, OcrSpider, OcrResponse, 
                         OcrRequest)

    app_id = 'xxxx'
    api_key ='xxxx' 
    secret_key = 'xxxx'

    img = ".\test.jpg"
    img2 = ".\test2.png"
    img3 = r'http://static.zongheng.com/upload/cover/07/f9/07f9c3d9899a7df6284c1d340d45ba8c.jpeg'
        
    class OcrItem(Item):
        title = OcrField(re_select=r'.*')

    class MySpider(OcrSpider):

        ocr_service = BaiduOcrService(app_id, api_key, secret_key)

        # ocr_region:str  x1,y1,x2,y2;...
        # default: '' means  the whole picture to ocr
        # 1,1,0.5,0.5 means: cut from image 1,1, image.width * 0.5, image.height * 0.5
        # 1,1,200,200 means: cut from image 1,1,200,200 
        # 1,1,0.5,0.5;0.5,0.5,0.99,0.99 means: 
        #   cut from image 1,1,image.width * 0.5, image.height * 0.5 get image1  
        #   cut from image image.width*0.5, image.height*0.5 ,image.width*0.99, image.height*0.99  get image2
        #   stitching image1 image2 by row get new image to ocr
        ocr_region = '1,1,0.5,0.99'

        start_urls = [img, img2, img3]

        concurrency = 1

        async def parse(self, response: OcrResponse):
            item = await OcrItem.get_item(html=await response.text())
            return item



            

    if __name__ == '__main__':
        MySpider.start()

