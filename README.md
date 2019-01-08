## ask39 spider

> based on scrapy.
>
> 195845 -> 8679 (0.0443)
>
> 1047300 -> 220879 (0.210)
>
> 50000000 ~ (大约是百万级)
>
> nohup: url: http://ask.39.net/question/3840308.html 3840293
>
> 622065
>
> 3840293 -> 622065 (0.16)



### question item

> url template: 'http://ask.39.net/question/%s.html' % page_num
>
> page_num: 1 - 60000000

```Python
q_id = Field()  # question id
d_id = Field()  # doctor id
sub = Field() # 
title = Field()  # title
gender = Field()  # gender
age = Field()  # age
onset = Field()  # time of onset
labels = Field()  # labels
query = Field()  # query
response = Field()  # including zw
```





### doctor item

> url template:  'http://my.39.net/%s' % doctor_id
>
> eg: P4349188git push -u origin master

```Python
d_id = Field()  # doctor id
d_name = Field()  # doctor name
d_job = Field()  # doctor job
d_hospital = Field()  # hospital of doctor
d_department = Field()  # department of doctor
d_excel = Field()  # good at
d_about = Field()  # about
```



### user agents

> user Agents: https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/4





