from django.shortcuts import render

# Create your views here.


from django.shortcuts import HttpResponse
from django.shortcuts import render  # 替代open文件读取
from django.shortcuts import redirect  # 跳转
import json

from cmdb import models  # 数据库

def auth(func):
    def inner(request, *args, **kwargs):
        val = request.COOKIES.get("email-cookies")
        if not val:
            return redirect('/cmdb/login')
        return func(request, *args, **kwargs)
    return inner



def login(request):  # request 包含用户提交的所有信息
    error_msg = ""
    ret = {"status": True, "error": None, "data": None}
    response = ""

    if request.method == "GET":
        val = request.COOKIES.get("email-cookies")
        if val:
            return redirect("/cmdb/admin")

        return render(request, 'index.html')

    elif request.method == "POST":  # request.method 获取请求方式
        try:
            user = request.POST.get('user', None)
            pwd = request.POST.get('pwd', None)

            print(user, pwd)

            result = models.UserInfo.objects.filter(email=user, password=pwd)

            print(result.query)

            if len(result) == 0:
                ret["status"] = False
                ret["error"] = "用户名或密码错误"

                print("邮箱未注册")

            # else:
            #     return redirect('/EOMS/admin')
        except Exception as e:
            ret["status"] = False
            ret["error"] = "请求错误：" + "%s" % e

        print(ret)

        response = HttpResponse(json.dumps(ret))

        if ret["status"]:
            # 设置cookie， 关闭游览器失效
            response.set_cookie('email-cookies', user, max_age=86400)

        return response
        # return HttpResponse(json.dumps(ret))


def register(request):
    error_msg = ""
    msg_code = ""

    if request.method == "POST":  # request.method 获取请求方式
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        confirm_pwd = request.POST.get('confirm_pwd', None)
        try:
            result = models.UserInfo.objects.filter(email=user)  # 查询用户名
            print(result.query)
            if len(result) == 0:
                if pwd == confirm_pwd:
                    models.UserInfo.objects.create(email=user, password=pwd)  # 增加数据
                    print("邮箱：%s注册成功！" % (user))
                    msg_code = "001"
                    Dict = {'msg_code': msg_code}
                    error_msg = "注册成功！"
                    return render(request, 'register.html', {'error_msg': error_msg, 'Dict': json.dumps(Dict)})
                else:
                    error_msg = "两次密码输入不一致！"
            else:
                error_msg = "邮箱已注册！"
        except Exception as e:
            print(e)

    return render(request, 'register.html', {'error_msg': error_msg})

@auth
def admin(request):  # request 包含用户提交的所有信息
    return render(request, 'admin.html')

@auth
def hosts(request):
    # hosts = ""
    ret = {"status": True, "error": None, "data": None, "type": None}

    if request.method == "GET":
        hosts_info = models.Hosts.objects.all().values("id", "hostname", "ip", "port", "business__name")
        businesses = models.Business.objects.all().values("id", "name")

        response = render(request, 'hosts.html', {'hosts': hosts_info, "businesses": businesses})
        response['X-Application-Name'] = "EOMS"  # 自定义响应头
        return response

    elif request.method == "POST":
        _type = request.POST.get("_type")

        if _type == "add_host":
            ret["type"] = "add_host"
            try:
                hostname = request.POST.get("hostname")
                ip = request.POST.get("ip")
                port = request.POST.get("port")
                business_id = request.POST.get("business")

                print(hostname, ip, port, business_id)

                if len(hostname) == 0 and len(ip) == 0 or len(port) == 0 or len(business_id) == 0:
                    ret["status"] = False
                    ret["error"] = "字段不能为空"
                else:
                    models.Hosts.objects.create(hostname=hostname, ip=ip, port=port, business_id=business_id)
            except Exception as e:
                ret["status"] = False
                ret["error"] = "请求错误：" + "%s" % e

            print(ret)

        elif _type == "del_host":
            print("删除开始-->")
            ret["type"] = "del_host"
            try:
                _id = request.POST.get("_id")
                print(_id)

                if len(_id) == 0:
                    ret["status"] = False
                    ret["error"] = "字段不能为空"
                else:
                    models.Hosts.objects.filter(id=_id).delete()
                    #print(_id)
            except Exception as e:
                ret["status"] = False
                ret["error"] = "请求错误：" + "%s" % e

        response = HttpResponse(json.dumps(ret))   # 序列化并向前端返回
        return response