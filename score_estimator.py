import argparse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://movie.douban.com/subject/"

def parse_args():
    parser = argparse.ArgumentParser(description="args for douban score estimator")
    parser.add_argument("subject_id", type=str, default=None, help="douban subject id")
    args = parser.parse_args()
    return args

def estimate_score(subject_id):
    url = BASE_URL + str(subject_id) + "/comments?status=P"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"} 
    req = Request(url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html.decode('utf-8'), "html.parser")

    # 1. Get the number of short comments
    command_meta = soup.find("ul", attrs={"class": "fleft CommentTabs"})
    command_meta = command_meta.find("li")
    short_command_num = int(command_meta.find("span").get_text()[3:-1])
    print("找到短评数量: ", short_command_num)

    # 2. Traverse through all the short commend scores to get the average score
    start_num = 0
    batch_size = 100
    total_score = 0
    score_dict = {1:0, 2:0, 3:0, 4:0, 5:0}
    for start_num in tqdm(range(0, short_command_num, batch_size), desc="获取分数"):
        try:
            url = BASE_URL + str(subject_id) + "/comments?start=" + str(start_num) + "&limit=" + str(batch_size) + "&status=P"
            req = Request(url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html.decode('utf-8'), "html.parser")
            score_dict[1] += len(soup.find_all("span", attrs={"class": "allstar10 rating"}))
            score_dict[2] += len(soup.find_all("span", attrs={"class": "allstar20 rating"}))
            score_dict[3] += len(soup.find_all("span", attrs={"class": "allstar30 rating"}))
            score_dict[4] += len(soup.find_all("span", attrs={"class": "allstar40 rating"}))
            score_dict[5] += len(soup.find_all("span", attrs={"class": "allstar50 rating"}))
        except:
            break
    valid_num = score_dict[1] + score_dict[2] + score_dict[3] + score_dict[4] + score_dict[5]
    print("有效短评数量: ", valid_num)
    print("星星分布: ", score_dict)
    total_score = score_dict[1] + score_dict[2]*2 + score_dict[3]*3 + score_dict[4]*4 + score_dict[5]*5
    total_score = total_score / valid_num
    print(f"平均分: {total_score * 2:.1f} / 10")


if __name__=="__main__":
    args = parse_args()
    subject_id = args.subject_id
    estimate_score(subject_id)