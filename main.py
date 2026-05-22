from datetime import date, datetime
import requests
import os

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
webhook_url = os.environ.get(
  "WECHAT_WORK_WEBHOOK",
  "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a0d392fd-a5dc-4ae7-8d41-1837e31caf84"
)


def get_weather():
  #url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  url = "https://query.asilu.com/weather/weather?action=weather/weather/&id=101010100"
  res = requests.get(url).json()
  weather = res['list'][0]
  return weather['weather'], weather['temp']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']


def build_message(weather, temperature, love_days, birthday_left, words):
  return "\n".join([
    "## \u6bcf\u65e5\u63a8\u9001",
    "",
    f"> \u57ce\u5e02\uff1a{city}",
    f"> \u5929\u6c14\uff1a{weather}",
    f"> \u6e29\u5ea6\uff1a{temperature}",
    f"> \u5728\u4e00\u8d77\uff1a<font color=\"info\">{love_days}</font> \u5929",
    f"> \u8ddd\u79bb\u751f\u65e5\uff1a<font color=\"warning\">{birthday_left}</font> \u5929",
    "",
    words
  ])


def send_group_message(content):
  payload = {
    "msgtype": "markdown",
    "markdown": {
      "content": content
    }
  }
  response = requests.post(webhook_url, json=payload, timeout=10)
  response.raise_for_status()
  return response.json()


wea, temperature = get_weather()
message = build_message(wea, temperature, get_count(), get_birthday(), get_words())
res = send_group_message(message)
print(res)
