如果你正在用扇贝背单词，`shanbay wordbook` 可以帮助你整理出这本单词书的音频文件，包括中文翻译。

#	Usage

1.	免登陆

	无需登陆。只需要将第8行的`userid`换成你自己的user-id，也就是`我的打卡`页面的链接地址中最后的那一串数字。比如如下链接的[user-id]就是`12345678`

		https://www.shanbay.com/checkin/user/12345678/

2.	单词书编号

	将第9行的`bookid`换成你的单词书编号。打开你收藏的某本单词书，链接中的最后一串数字就是单词书编号。比如[sherlock holmes 第一季／第一集-1](https://www.shanbay.com/wordbook/1366/)这本单词书的链接是

		https://www.shanbay.com/wordbook/1366/

	那么`bookid`就是`1366`。注意只能下载已收藏的单词书，否则可能会出现找不到资源的情况。

3.	发音间隔

	`res`文件夹中的`/blank.mp3`是一段时长`0.5s`的空白音频，作为两段发音之间的衔接。

3.	依赖工具

	*	`python3.4` 与 `pip3`

		[www.python.org](https://www.python.org/)

	*	`requests`

		```bash
		$ pip3 install requests
		```

	*	`BeautifulSoup`

		```bash
		$ pip3 install beautifulsoup4
		```

	*	`ffmpeg` 或 `avconv`

		因为中文翻译的音频与英文的音频比特率不同，如果要合en-cn形式的音频，则需要借助ffmpeg。

		如果只需要英文发音，那么首先把第89行注释掉

		```python3
		shell("cat _en.mp3 _cn.mp3 blank.mp3 >> _" + filename + ".mp3", shell=True)
		```

		然后取消第90行的注释

		```python
		# shell("cat _en.mp3 blank.mp3 >> _" + filename + ".mp3", shell=True)
		```

4.	延时

	注意应对反爬虫机制，代码中简单地使用了延时。需要根据具体情况设定与调整。同时也是考虑不给服务器造成太大压力。为人为己。

	```python
	time.sleep(3)
	```

5.	试听效果

	在`res`文件夹中

	*	`01_`开头的文件是第3点提到的空白片段
	*	`02_`开头的文件是未经处理的音频
	*	`03_`开头的文件是最终效果，包含两个单词的中英文发音

6.	仅用于个人学习，请勿用于商业用途。
