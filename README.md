# douban_score_estimator

一个简单的Python脚本
用来在电影正式出分之前预估一下评分

## Usage
```
python3 score_estimator ${MOVIE_ID}
```

## Limitation

直接爬取豆瓣页面似乎只能获得前600条左右的短评分数，更多的豆瓣分数似乎是被拒绝访问的。