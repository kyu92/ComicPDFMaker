from os import path as os_path, listdir as os_listdir
from PIL import Image
from threading import Thread


def thread_it(func, *args):
    # 创建
    t = Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    t.join()


def set_log(widget, contect) -> None:
    widget.set_log(contect)


def get_dirs(path) -> list:
    target_path = path
    divide_char = ''
    if '\\' in target_path:
        divide_char = '\\'
    elif '/' in target_path:
        divide_char = '/'
    else:
        print("请输入正确的文件目录")
        raise FileNotFoundError
    # print(divide_char)
    if not path[-1] == divide_char:
        target_path = "%s%s" % (path, divide_char)
    dirs = list()
    for each in os_listdir(path):
        dirs.append("%s%s" % (target_path, each))
    return dirs


def read_files(path):
    if os_path.isdir(path):
        file_list = os_listdir(path)
        return file_list
    elif os_path.isfile(path):
        return "该路径下包含的是文件而非目录"


def rea(files, pdf_name, widget=None):
    # print(pdf_name)
    file_list = files
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)

    pic_name.sort()
    new_pic = []

    for x in pic_name:
        if "jpg" in x:
            new_pic.append(x)

    for x in pic_name:
        if "png" in x:
            new_pic.append(x)

    print("hec", new_pic)
    if widget is not None:
        thread_it(set_log, widget, list(map(lambda file: f"添加文件:{file}", new_pic)))
    if len(new_pic) > 0:
        try:
            im1 = Image.open(new_pic[0])
        except OSError:
            pdf_name = "%s%s.pdf" % (pdf_name[:pdf_name.rindex('.')], "-有缺损")
            print(f"读取到{new_pic[0]}时发生错误,已跳过该文件")
            if widget is not None:
                thread_it(set_log, widget, f"读取到{new_pic[0]}时发生错误,已跳过该文件")
        new_pic.pop(0)
        for i in new_pic:
            img = Image.open(i)
            if img.mode == "RGBA":
                img = img.convert('RGB')
                print(f"读取到{new_pic[0]}时发生颜色模式转换(RGBA -> RGB)")
                if widget is not None:
                    thread_it(set_log, widget, f"读取到{new_pic[0]}时发生颜色模式转换(RGBA -> RGB)")
                im_list.append(img)
            else:
                im_list.append(img)
        print(pdf_name[8:])
        im1.save(pdf_name[8:], "PDF", resolution=100.0, save_all=True, append_images=im_list)
        # print("输出文件名称：%s" % pdf_name[pdf_name.rindex('/') + 1:])
        if widget is not None:
            thread_it(set_log, widget, f"输出文件名称：{pdf_name[pdf_name.rindex('/') + 1:]}")