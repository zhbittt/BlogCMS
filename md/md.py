from django.conf import settings
from django.shortcuts import redirect
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class M1(MiddlewareMixin):

    def process_request(self,request):
        # 无返回值：继续执行后续中间件和视图函数
        # 有返回值：执行自己的process_response和上面的response
        # request.xxxx= 888
        # request.path_info # /login/
        if request.path_info == "/login/":
            return None

        # user_info = request.session.get(settings.SJF)
        # if not user_info:
        #     return redirect('/login/')


    def process_response(self,request,response):
        # print('m1.process_response')
        # print("md-------------------------------------------------------request",request)
        # print("md-------------------------------------------------------response",response)
        # print("-------------------------------------------------------print(request.session.items())",request.session.items())
        # print("md-------------------------------------------------------request.session.get(settings.REFER)",request.session.get("refer"))

        # if request.session.get("refer"):
        #     return redirect(request.session.get("refer"))
        return response

#
# class M2(MiddlewareMixin):
#
#     def process_request(self,request):
#         print('m2.process_request')
#
#
#     def process_response(self,request,response):
#         print('m2.process_response')
#         return response