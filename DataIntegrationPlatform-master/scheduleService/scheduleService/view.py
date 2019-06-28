from django.http import HttpResponse

from django.shortcuts import render


def hello(request):
    # 直接返回数据，数据与视图混合在一起
    # return HttpResponse("Hello world ! ")

    # 使用模板返回数据，实现数据与视图分离
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)
