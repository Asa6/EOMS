<h1>EOMS</h1>   

[![](https://travis-ci.org/Alamofire/Alamofire.svg?branch=master)](https://travis-ci.org/Asa6/EOMS)
[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)


<br />

开发环境


        django 2.0.5 
        PyMySQL 0.9.2
        django-redis 4.9.0


运行环境
             
        nginx + gunicorn + django + mysql + redis



生成表

        python manage.py makemigrations
        python manage.py migrate



额外操作

        python manage.py makemigrations --empty 应用名
        python manage.py migrate --fake  # 如果有删除表或更改表名时先执行这一句


