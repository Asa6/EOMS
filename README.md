<h1>EOMS</h1>   

[![](https://travis-ci.org/Alamofire/Alamofire.svg?branch=master)](https://travis-ci.org/Asa6/EOMS)
[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)


<br />

开发环境

        python 3.6
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

其他操作

        python manage.py sqlmigrate cmdb 0001   # 查看cmdb app的建表sql
        
        python manage.py dumpdata cmdb > cmdb_dump.json   #导出cmdb app的数据
        python manage.py migrate --fake  # 导入cmdb app的数据

