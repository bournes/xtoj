import json
import os
import sys

import app_thread


class appLogic():
    def __init__(self):
        self.xls_path = ""
        self._start()

    # 初始化数据
    def _start(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', encoding='utf-8') as f:
                    content = json.load(f)
                    f.close()
                    # xls 路径
                    self.xls_path = content['xls']['url']
                    # xls 主键ID 惯例是第一列"id" 不能重复
                    self.xls_key_id = content['xls']['key_id']
                    # xls 字段类型开始行
                    self.xls_type_from = content['xls']['type_from']
                    # xls 导出规则开始行
                    self.xls_rule_from = content['xls']['rule_from']
                    # xls 字段开始行
                    self.xls_key_from = content['xls']['key_from']
                    # xls 内容开始行
                    self.xls_content_from = content['xls']['content_from']
                    # 导出前端json 路径
                    self.outClientJson = content['outClientJson']['url']
                    # 导出前端TS 路径
                    self.outClientTs = content['outClientTs']['url']
                    # 导出后端json 路径
                    self.outServerJson = content['outServerJson']['url']
                    # 导出后端Go 路径
                    self.outServerGo = content['outServerGo']['url']

                    self._gen_btn_click()
            else:
                print("必须先配置好配置文件才能继续。。。。。。")
        except:
            print(sys.exc_info())

    # 获取所有文件
    def file_name(self, dir):

        L = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                if os.path.splitext(file)[1] == '.xlsx':
                    file_name = os.path.splitext(file)[0]
                    file_path = os.path.join(root, file)
                    file_parent = os.path.dirname(file_path)
                    if file_name[0][0] != "~":
                        L.append([file_name, file_path, file_parent])

        return L

    # 生成
    def _gen_btn_click(self):
        try:

            file = self.file_name(self.xls_path)
            # 没有目录自动创建,原理上不应该为空，但是如果是配置文件下，就有可能
            if not os.path.exists(self.outClientJson):
                os.mkdir(self.outClientJson)
            if not os.path.exists(self.outClientTs):
                os.mkdir(self.outClientTs)
            if not os.path.exists(self.outServerJson):
                os.mkdir(self.outServerJson)
            if not os.path.exists(self.outServerGo):
                os.mkdir(self.outServerGo)
            # 先清理下目录
            self.del_file(self.outClientJson)
            self.del_file(self.outClientTs)
            self.del_file(self.outServerJson)
            self.del_file(self.outServerGo)

            app_thread.AppThread(file, self.outClientJson, self.outClientTs, self.outServerJson, self.outServerGo,
                                 self.xls_key_id, self.xls_type_from, self.xls_rule_from, self.xls_key_from,
                                 self.xls_content_from).run()


        except:
            print(sys.exc_info())

    #  清空目录
    def del_file(self, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)


if __name__ == '__main__':
    appLogic()
