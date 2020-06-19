class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const ()")
        self.__dict__[name] = value


Const = _const()
Const.HELP = "帮助"
Const.HELP_STR = '''使用方式：
选择文件夹后输入文件名即可，
注：文件夹内的结构请严格按照要求来：
    1、文件夹内可以有多个文件夹，每个文件夹代表内必须是图片文件，即每个文件夹一话
    2、最终输出的文件是一个pdf，也就是说选择的文件夹内集数越多pdf包含的内容也越多
    3、当前本软件还在测试中
'''
Const.QSS = '''
#files_list{
    background: transparent;
    border-radius: 5px;
    border: 1.5px solid rgba(255, 63, 72, 0.8);
    color: red;
}

#log_box{
    background: transparent;
    border-radius: 5px;
    border: 1.5px solid rgba(255, 63, 72, 0.8);
}

#select_files_btn {
    border: 3px solid rgba(255, 141, 36, 0.8);
    border-radius: 23px;
    color: red;
    background: transparent;
    height: 3em;
    text-align: center;
    width: 10em;
    padding:2px 4px;
}

#select_files_btn:hover {
    color: black;
    border: 3px solid rgba(0, 0, 0, 0.8);
    font-weight: bold;
}

#widget_title_files_list{
    color: red;
    font-weight: bold;
}

#widget_title_log{
    color: red;
    font-weight: bold;
}

#help_window{
    border-image: url("HelpWindowBody.png");
    /*background: transparent;*/
}
'''
