import requests
import ddddocr


# 失败后随机 1-2s 后重试，最多 5 次
@retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=5)
def get_img(ocr,driver):
    """
    获取最新的一张验证码图片，并返回识别结果
    :param ocr: 识别验证码库实例
    :param driver: 驱动实例，获取cookie
    :return res:识别结果
    """
    cookies=driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
    try:
        res =  s.get(url, timeout=3) #设置超时时间为3s
        logging.info('下载验证码图片成功')
    except:
        logging.error('下载验证码图片失败')
        raise Exception('下载验证码图片失败')

    with open('captcha.jpg',"wb") as f:
        f.write(res.content)

    with open('captcha.jpg', 'rb') as f:
        img_bytes = f.read()
    try:
        res = ocr.classification(img_bytes)
        logging.info('验证码识别成功：'+str(res))
    except:
        logging.error('验证码识别失败')
        raise Exception('验证码识别失败')
    return res


def wx_send(wxsend_key, message):
    data = {
        "text": "健康申报结果"+message,
        "desp": "如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。"
    }
    try:
        r = requests.post(f'https://sc.ftqq.com/{wxsend_key}.send', data = data)
        if r.status_code == 200:
            print('发送通知成功')
        else:
            print('发送通知失败')
    except:
        print('发送通知失败')
