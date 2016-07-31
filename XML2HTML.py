from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

''''''


def printname(func):
    def wrapper(*args, **kw):
        print('call:    %s()' % func.__name__)
        return func(*args, **kw)
        # pass
    return wrapper
    # pass


class Dispatcher:
    """工厂模式的工厂"""
    #@printname
    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        # 根据读取到的xml标签，使用getattr获取方法，采取不同的操作。
        method = getattr(self, mname, None)
        # callable 返回函数是否可以调用
        if callable(method):
            args = ()  # 新建一个tuple
        else:
            method = getattr(self, dname, None)
            args = name,
        if prefix == 'start':
            args += attrs,  # attrs为startElement解析xml得出的xml节点对象
        if callable(method):
            method(*args)

            #print('call:  %s()' % method.__name__)
    # 初始化以后最先执行的方法，此方法为操作类的接口，两个方法都为触发事件
    @printname
    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    @printname
    def endElement(self, name):
        self.dispatch('end', name)

# 继承Dispatcher实现工厂模式，继承ContentHandler为xml的操作类
# 采用MixIn,多重继承


class WebsiteConstructor(Dispatcher, ContentHandler):
    """工厂模式的实现方式"""
    passthrough = False

    @printname
    def __init__(self, directory):
        self.directory = [directory]
        self.ensureDirectory()

    @printname
    def ensureDirectory(self):
        path = os.path.join(*self.directory)

        if not os.path.isdir(path):
            os.makedirs(path)
            # print(path)
            # print('----')

    @printname
    def characters(self, chars):
        if self.passthrough:
            self.out.write(chars)

    @printname
    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' %s="%s"' % (key, val))
            self.out.write('>')

    @printname
    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write('</%s>' % name)

    @printname
    def startDirectory(self, attrs):
        # print(attrs['name'] + ':StartDirectory')
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    @printname
    def endDirectory(self):
        # print('endDirectory')
        self.directory.pop()

    @printname
    def writeHeader(self, title):
        self.out.write('<html>\n<head>\n   <title>')
        self.out.write(title)
        self.out.write('</title>\n </head>\n <body>\n')

    @printname
    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')

    @printname
    def startPage(self, attrs):
        # print('startPage')
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True

    @printname
    def endPage(self):
        # print('endPage')
        self.passthrough = False
        self.writeFooter()
        self.out.close()
# WebsiteConstructor('public_html') 作为parse的操作方式传入
parse('website.xml', WebsiteConstructor('public_html'))
