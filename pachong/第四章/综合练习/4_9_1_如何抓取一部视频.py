# <video src="不能播的视频.mp4"></video>
# 一般的视频网站是怎么做的?
# 用户上传 -> 转码(把视频做处理, 2K, 1080, 标清)  -> 切片处理(把单个的文件进行拆分)  60
# 用户在进行拉动进度条的时候
# =================================

# 需要一个文件记录: 1.视频播放顺序, 2.视频存放的路径.
# M3U8  txt  json   => 文本
# M3U8 是 M3U 编码为 UTF-8 之后得来的
# 是文本，就可以用 open("fileName", mode="w", encoding="UTF-8") 来写入

# 想要抓取一个视频:
#  1. 找到m3u8 (各种手段)
#  2. 通过m3u8下载到ts文件
#  3. 可以通过各种手段(不仅是编程手段) 把ts文件合并为一个mp4文件

"""
M3U8 文件：

#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:5                    <- 这个是每个视频切片的最大时长
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-KEY:METHOD=AES-128,URI="key.key"    <- 这个是切片文件的加密方式以及密钥地址，如果有加密，需要先解密才能播放
#EXT-X-PLAYLIST-TYPE:VOD
#EXTINF:4.004267,
https://m3api.awenhao.com/phls/MTZmY
#EXTINF:2.002133,                          <- EXTINF 就是每个切片的持续时间
https://m3api.awenhao.com/phls/NWE5N
#EXTINF:3.628867,
https://m3api.awenhao.com/phls/NWE3Z       <- 这个是每个切片文件的地址
#EXTINF:4.004267,
https://m3api.awenhao.com/phls/ZmNiZ
#EXTINF:2.002133,
https://m3api.awenhao.com/phls/YzNjN
#EXTINF:4.004267,
https://m3api.awenhao.com/phls/MWM1O
#EXTINF:2.002133,
https://m3api.awenhao.com/phls/NzYxZ
#EXTINF:4.004267,
https://m3api.awenhao.com/phls/ODhjZ
#EXTINF:2.002133,
......
https://m3api.awenhao.com/phls/YjAyM
#EXT-X-ENDLIST
"""
