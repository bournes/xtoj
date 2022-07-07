# -*- coding: utf-8 -*-
# 逻辑线程
# by jhj QQ8510001 2022-7-7
import codecs
import json
import sys
import threading
import time
import warnings
from openpyxl import load_workbook
import traceback


class AppThread():

    def __init__(self, file, outClientJson, outClientTs, outServerJson, outServerGo,xls_key_id,xls_type_from,xls_rule_from,xls_key_from,xls_content_from):
        super(AppThread, self).__init__()
        self.file_list = file
        self.outClientJson = outClientJson
        self.outClientTs = outClientTs
        self.outServerJson = outServerJson
        self.outServerGo = outServerGo
        # xls 主键
        self.xls_key_id = xls_key_id
        # xls 字段类型开始行
        self.xls_type_from = xls_type_from
        # xls 导出规则开始行
        self.xls_rule_from = xls_rule_from
        # xls 字段开始行
        self.xls_key_from =xls_key_from
        # xls 内容开始行
        self.xls_content_from = xls_content_from

    def run(self):
        try:
            if not self.file_list:
                print("文件为空，线程不工作")
                return

            for f in self.file_list:
                threading.Thread(target=self._gen_json, args=([f])).start()

            # 单独开一个线程写GO的总文件
            threading.Thread(target=self.genConfigGo, args=([self.file_list])).start()

        except:
            print(sys.exc_info())

    def _gen_json(self, f):

        try:
            warnings.simplefilter("ignore")
            t0 = time.time()

            wb = load_workbook(f[1], read_only=True, data_only=True)
            worksheets = wb.sheetnames
            if worksheets[0] == None:
                return  # 第一个表单没有就终端

            out_file_name = f[0]
            ws = wb[worksheets[0]]

            if ws.max_row == 1 and ws.max_column == 1:
                return  # 没有内容退出

            # 建立存储数据的字典
            # print("当前最大行", ws.max_row, '当前最大列数', ws.max_column)

            # # 因为按行，所以返回A1, B1, C1这样的顺序
            key = {}
            skey = {}
            rule = {}
            type_rule = {}
            data_dict_f = {}
            sdata_dict_f = {}
            error = 0
            i = 0
            for row in ws.rows:
                temp_list_f = {}
                stemp_list_f = {}
                i = i + 1
                j = 0
                for cell in row:
                    j += 1
                    if i == self.xls_type_from:  #  type

                        if cell.value is not None:
                            # print("type_rule规则", cell.value, j)
                            type_rule[j] = str(cell.value)

                        else:
                            continue

                    if i == self.xls_rule_from:  #  rule
                        if cell.value is not None:
                            # print("前端 后端 或略规则", cell.value, j)
                            rule[j] = str(cell.value)

                        else:
                            continue

                    if i == self.xls_key_from:  #  key

                        if cell.value is not None:
                            if str(rule[j]).lower() == "client" or str(rule[j]).lower() == "both":
                                # 容错判断下这个键位的规则有没有
                                if j in type_rule:
                                    # print("导出Client", cell.value, j, rule[j])
                                    key[j] = str(cell.value)
                                else:
                                    error += 1

                            if str(rule[j]).lower() == "server" or str(rule[j]).lower() == "both":
                                # 容错判断下这个键位的规则有没有
                                if j in type_rule:
                                    # print("导出Server", cell.value, j, rule[j])
                                    skey[j] = str(cell.value)
                                else:
                                    error += 1

                        else:
                            break

                    if i >= self.xls_content_from:  # 内容
                        if j <= len(rule):
                            if j in key:
                                if cell.value is None:
                                    temp_list_f[key[j]] = 0
                                else:
                                    temp_list_f[key[j]] = str(cell.value)
                            if j in skey:
                                if cell.value is None:
                                    stemp_list_f[skey[j]] = 0
                                else:
                                    stemp_list_f[skey[j]] = str(cell.value)



                if temp_list_f != {}:
                    data_dict_f[temp_list_f[self.xls_key_id]] = temp_list_f
                if stemp_list_f != {}:
                    sdata_dict_f[stemp_list_f[self.xls_key_id]] = stemp_list_f



            if data_dict_f:
                # client json
                self.write_file(self.outClientJson + "/" + out_file_name + ".json", data_dict_f)
                # client ts
                # print(key)
                # print(type_rule)
                self.gents(out_file_name, key, type_rule)

                del temp_list_f
                del data_dict_f
            if sdata_dict_f:
                # server json
                self.write_file(self.outServerJson + "/" + out_file_name + ".json", sdata_dict_f)
                # server go
                self.gengo(out_file_name, skey, type_rule)

                del stemp_list_f
                del sdata_dict_f

            t1 = time.time()
            if error > 0:
                print(out_file_name + " 导出完毕！！ 行：", ws.max_row, '列：', ws.max_column, " 耗时：" + str(t1 - t0),
                      "[有错误未定义类型：" + str(error) + "]")
            else:
                print(out_file_name + " 导出完毕！！ 行：", ws.max_row, '列：', ws.max_column, " 耗时：" + str(t1 - t0))

        except:
            print("配置表错误！")
            print(f[0], sys.exc_info())
            print("key", key)
            print("type", type_rule)
            traceback.print_tb(sys.exc_info()[2])

    def write_file(self, filename, buf):
        totxt = codecs.open(filename, 'w', "utf-8")
        totxt.write(str(json.dumps(buf)))
        totxt.close()

    def gents(self, file, key, type_rule):
        version = '3.4'

        # 生成TS文件
        ts_waring = '/**\n * @导出自 ' + file + '.xls\n * @此文件为自动导出 请勿修改\n * @导出时间 ' + time.strftime('%Y.%m.%d',
                                                                                                  time.localtime(
                                                                                                      time.time())) + '\n * @导出工具 v' + version + ' \n * @Author jhj \n * @QQ 8510001 \n */ \n'
        # 字段
        field = ""
        for k in key:
            if key[k] != 'id':
                field += '\n    get ' + self.toSmaillWord(key[k]) + '(): ' + self.changetype(
                    type_rule[k]) + ' { \n        return this.data.' + key[k] + ';\n    }\n'

        script = ts_waring + 'import {JsonUtil} from  "../../../core/utils/JsonUtil"; \n\n' \
                 + 'export class Table' + self.toBigWord(file) + ' {\n' \
                 + '    static TableName: string = "' + file + '";\n' \
                 + '    private data: any;\n\n' \
                 + '    init(id: number) {\n' \
                 + '        let table = JsonUtil.get(Table' + self.toBigWord(file) + '.TableName);\n' \
                 + '        this.data = table[id];\n' \
                 + '        this.id = id;\n    }\n\n' \
                 + '    id: number = 0;\n' \
                 + field + '\n}'

        totxt_b = codecs.open(self.outClientTs + '/' + file + '.ts', 'w', "utf-8")
        totxt_b.write(script)
        totxt_b.close()

    def changetype(self, type):
        if type.lower() == 'int':
            return 'number'
        else:
            return type

    def changeInt(self, type):
        if type.lower() == 'int':
            return 'uint32'
        else:
            return type

    def gengo(self, file, key, type_rule):
        version = '3.4'

        # 生成TS文件
        ts_waring = '/**\n * @导出自 ' + file + '.xls\n * @此文件为自动导出 请勿修改\n * @导出时间 ' + time.strftime('%Y.%m.%d',
                                                                                                  time.localtime(
                                                                                                      time.time())) + '\n * @导出工具 v' + version + ' \n * @Author jhj \n * @QQ 8510001 \n */ \n'
        # 字段
        field = ""
        for k in key:
            # print(key[k],type_rule[k])
            field += '	' + self.toBigWord(key[k]) + '  ' + self.changeInt(type_rule[k]) + '  `json:"' + key[
                k] + '"`\n'

        script = ts_waring + 'package configdef \n\ntype ' + self.toBigWord(
            file) + ' struct {\n' + field + '}\n\nvar ' + self.toBigWord(file) + 'M  map[string]*' + self.toBigWord(
            file)
        totxt_b = codecs.open(self.outServerGo + '/' + file + '.go', 'w', "utf-8")
        totxt_b.write(script)
        totxt_b.close()

    # 下划线转大驼峰
    def toBigWord(self, word):
        out = ""
        if "_" in word:
            for w in word.split("_"):
                out += w.capitalize()

        else:
            return word.capitalize()

        return out

    # 下划线转小驼峰
    def toSmaillWord(self, word):
        out = ""
        if "_" in word:
            for w in word.split("_"):
                if w != word.split("_")[0]:
                    out += w.capitalize()
                else:
                    out += w

        else:
            return word

        return out

    def genConfigGo(self, filelist):
        version = '3.4'

        # 生成TS文件
        ts_waring = '/**\n * @此文件为自动导出 请勿修改\n * @导出时间 ' + time.strftime('%Y.%m.%d', time.localtime(
            time.time())) + '\n * @导出工具 v' + version + ' \n * @Author jhj \n * @QQ 8510001 \n */ \n'

        # 字段
        field = ""
        for k in filelist:
            # print(k[0])
            field += '	case File' + self.toBigWord(k[0]) + ':\n		return &' + self.toBigWord(k[0]) + 'M\n'

        const = ""
        for k in filelist:
            const += '	File' + self.toBigWord(k[0]) + ' string = "' + k[0] + '.json"  \n'

        script = ts_waring + 'package configdef \n\nconst (\n   ' + const + ')\nfunc LoadStrut(fileName string) interface {}  {\n	switch fileName {\n  ' + field + '	default:\n		return nil\n	}\n}'
        totxt_b = codecs.open(self.outServerGo + '/configdef.go', 'w', "utf-8")
        totxt_b.write(script)
        totxt_b.close()
