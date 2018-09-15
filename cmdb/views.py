from django.shortcuts import render

# Create your views here.


from django.shortcuts import HttpResponse
from django.shortcuts import render  # 替代open文件读取
from django.shortcuts import redirect  # 跳转
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils.safestring import mark_safe

import json
from cmdb import models  # 数据库




# 用户认证装饰器
def auth(func):
    def inner(request, *args, **kwargs):
        if not request.session.get('is_login', None):
            return redirect('/cmdb/login')
        return func(request, *args, **kwargs)
    return inner


class Page:
    def __init__(self, current_page, data_count, page_count=10, pager_num=5):
        self.current_page = current_page
        self.data_count = data_count
        self.page_count = page_count
        self.pager_num = pager_num

    def start(self):
        return (self.current_page - 1) * self.page_count

    def end(self):
        return self.current_page * self.page_count

class Login(View):
    def __init__(self):
        self.ret = {"status": True, "error": None, "data": None}

    # request 包含用户提交的所有信息
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect("/cmdb/admin")

        return render(request, 'index.html')

    def post(self, request):
        try:
            user = request.POST.get('user', None)
            pwd = request.POST.get('pwd', None)

            print(user, pwd)

            result = models.UserInfo.objects.filter(email=user, password=pwd)

            print(result.query)

            if len(result) == 0:
                self.ret["status"] = False
                self.ret["error"] = "用户名或密码错误"

                print("邮箱未注册")
        except Exception as e:
            self.ret["status"] = False
            self.ret["error"] = "请求错误：" + "%s" % e

        print(self.ret)

        if self.ret["status"]:
                request.session['username'] = user
                request.session['is_login'] = True

        #     # 设置cookie， 关闭游览器失效
        #     response.set_cookie('email-cookies', user, max_age=86400)
        return HttpResponse(json.dumps(self.ret))


class Register(View):
    def __init__(self):
        self.error_msg = ""
        self.msg_code = ""

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
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


@method_decorator(auth, name="dispatch")
class Admin(View):
    def __init__(self):
        self.ret = {"status": True, "error": None, "data": None, "type": None}

    def get(self, request):
        return render(request, 'admin.html')

    def post(self, request):
        _type = request.POST.get("_type")

        if _type == "del_session":
            self.ret["type"] = "del_session"

            try:
                # 用户退出登录
                request.session.clear()
            except Exception as e:
                self.ret["status"] = False
                self.ret["error"] = "请求错误：" + "%s" % e

        response = HttpResponse(json.dumps(self.ret))
        return response

@method_decorator(auth, name="dispatch")
class Hosts(View):
    def __init__(self):
        self.ret = {"status": True, "error": None, "data": None, "type": None}

    def get(self, request):
        # 每页显示的数量
        page_count = 10

        # 页码个数
        pager_num = 5

        current_page = request.GET.get('page_number', 1)
        current_page = int(current_page)

        strat = (current_page - 1) * page_count
        end = current_page * page_count

        hosts_info = models.Hosts.objects.all().values("id", "hostname", "ip", "port", "business__name")
        businesses = models.Business.objects.all().values("id", "name")

        hosts_info = hosts_info[strat:end]
        businesses = businesses[strat:end]

        all_count = len(models.Hosts.objects.all())
        total_count, mod = divmod(all_count, page_count)

        if mod:
            total_count += 1

        page_list = []


        if total_count < pager_num:
            start_index = 1
            end_index = total_count + 1
        else:
            if current_page <= (pager_num + 1)/2:
                start_index = 1
                end_index = pager_num + 1
            else:
                start_index = current_page - (pager_num - 1)/2
                end_index = current_page + (pager_num + 1)/2
                if (current_page + (pager_num - 1)/2) > total_count:
                    end_index = total_count + 1
                    start_index = total_count - pager_num + 1


        if current_page <= 1:
            last_page = '<li class="disabled"><a href="javascript:void(0)">&laquo;</a></li>'
            page_list.append(last_page)
        else:
            last_page = '<li><a href="/cmdb/hosts?page_number=%s">&laquo;</a></li>' % (current_page - 1)
            page_list.append(last_page)

        for i in range(int(start_index), int(end_index)):
            if i == current_page:
                # temp = '<li class="active"><a href="/cmdb/hosts?page_number=%s">%s</a></li>' % (i, i)
                temp = '<li class="active"><a href="javascript:void(0)">%s</a></li>' % (i)
            else:
                temp = '<li><a href="/cmdb/hosts?page_number=%s">%s</a></li>' % (i, i)

            page_list.append(temp)

        # print(current_page, total_count)

        if current_page >= total_count:
            next_page = '<li class="disabled"><a href="javascript:void(0)">&raquo;</a></li>'
            page_list.append(next_page)
        else:
            next_page = '<li><a href="/cmdb/hosts?page_number=%s">&raquo;</a></li>' % (current_page + 1)
            page_list.append(next_page)

        page_str = "".join(page_list)
        page_str = mark_safe(page_str)

        response = render(request, 'hosts.html', {'hosts': hosts_info, "businesses": businesses, 'page_str': page_str})
        response['X-Application-Name'] = "EOMS"  # 自定义响应头
        return response

    def post(self, request):
        _type = request.POST.get("_type")

        if _type == "add_host":
            self.ret["type"] = "add_host"
            try:
                hostname = request.POST.get("hostname")
                ip = request.POST.get("ip")
                port = request.POST.get("port")
                business_id = request.POST.get("business")

                print(hostname, ip, port, business_id)

                if len(hostname) == 0 and len(ip) == 0 or len(port) == 0 or len(business_id) == 0:
                    self.ret["status"] = False
                    self.ret["error"] = "字段不能为空"
                else:
                    models.Hosts.objects.create(hostname=hostname, ip=ip, port=port, business_id=business_id)
            except Exception as e:
                self.ret["status"] = False
                self.ret["error"] = "请求错误：" + "%s" % e

            print(self.ret)

        elif _type == "del_host":
            print("删除开始-->")
            self.ret["type"] = "del_host"
            try:
                _id = request.POST.get("_id")
                print(_id)

                if len(_id) == 0:
                    self.ret["status"] = False
                    self.ret["error"] = "字段不能为空"
                else:
                    models.Hosts.objects.filter(id=_id).delete()
                    # print(_id)
            except Exception as e:
                self.ret["status"] = False
                self.ret["error"] = "请求错误：" + "%s" % e

        response = HttpResponse(json.dumps(self.ret))  # 序列化并向前端返回
        return response


class Page_not_found(View):
    def get(self, request):
        return render(request, '404.html')
