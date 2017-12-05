# comments= {
# 16: {'id': 16, 'content': '你哈奥啊', 'pid': None, 'children': []},
#
#
#
# 43: {'id': 43, 'content': '你写的文章都太棒了!!!', 'pid': None, 'children':
# [{'id': 60, 'content': '@jack写得太棒了。。。', 'pid': 43 ,'children': []},
#  {'id': 61, 'content': '这么棒谁写的。。。', 'pid': 43, 'children': []}]
#      },
#
#
# 44: {'id': 44, 'content': 'fdsafds', 'pid': None, 'children': []},
# 45: {'id': 45, 'content': 'avgfklsfjdklsfds', 'pid':None, 'children': []},
# 46: {'id': 46, 'content': 'vdsafds', 'pid': None, 'children': [{'id': 62, 'content': '@jack怎么有这么牛逼的文章！！', 'pid': 46, 'children': []}, {'id': 63, 'content': '太牛了吧。。', 'pid':46, 'children': []}, {'id': 64, 'content': '这个牛。。。', 'pid': 46, 'children': []}]},
#
#
# 60: {'id': 60, 'content': '@jack写得太棒了。。。', 'pid': 43, 'children': []},
# 61: {'id': 61, 'content': '这么棒谁写的。。。', 'pid': 43, 'children': []},
# 62: {'id': 62, 'content': '@jack怎么有这么牛逼的文章！！', 'pid': 46, 'children': []},
# 63: {'id': 63, 'content': '太牛了吧。。', 'pid': 46, 'children': []},
# 64: {'id': 64, 'content': '这个牛。。。', 'pid': 46, 'children': []}
# }
#
#
# commentss={
#     43: {'id': 43, 'content': '你写的文章都太棒了!!!', 'pid': None, 'children':
#     [{'id': 60, 'content': '@jack写得太棒了。。。', 'pid': 43 ,'children': []},
#      {'id': 61, 'content': '这么棒谁写的。。。', 'pid': 43, 'children': []}]
#          }
# }
# def fun(children):
#     c_list = []
#     # print("children------",children)
#     # print("c_list------",c_list)
#
#     for chil in children:
#         # print("chil",chil)
#         ret = fun(chil["children"])
#         # print("ret",ret)
#         if len(ret)==0:
#             c_list.append(chil)
#         # print("else-----------c_list",c_list)
#     else:
#         return c_list
#
#
# for comment_id in comments:
#     if comments[comment_id]["pid"] == None:
#         print("********************",fun(comments[comment_id]["children"]))





#####可迭代对象  iterator
'''
http://112.25.9.182:8088/hc.yinyuetai.com/uploads/videos/
common/972401601A855C00CD777F8DE20D480D.mp4?sc
=2f37e9bbf150e075&br=778&vid=3104718&aid=39901&area=
JP&vst=0&ptp=mv&rd=yinyuetai.com
'''
'''
//s.c.yinyuetai.com/swf/common/playerloader.swf?t=20170724
'''

# a = [1,2,3,4,5,6,7,8,9]
#
# b = a
#
# for x in b:
#     print(x)
#
# for x in b:
#     print(x)


dic={"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f"}

a = dic.items()

for x ,y in a:
    print(x,y)

for x ,y in a:
    print("---",x,y)