import datetime, os, re, json, math, random, time, requests, base64, os, pandas

from zhipuai import ZhipuAI
from zipfile import ZipFile
from bs4 import BeautifulSoup
from ordered_set import OrderedSet
from paddlenlp import Taskflow
from pdf2image import convert_from_path
from tqdm import tqdm
from PyQt6.QtCore import QObject, pyqtSignal


class JianLi(QObject):
    # Define custom signals
    resumeFiled = pyqtSignal(str)
    resumeParsed = pyqtSignal(dict)
    resumeVisiualParsed = pyqtSignal(pandas.core.frame.DataFrame)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._path = "./tmp/"
        # 设置实体抽取信息
        self.schema = [
            "姓名",
            "出生年月",
            "年龄",
            "最高学历",
            "毕业院校",
            "工作年限",
            "电话",
            "性别",
            "政治面貌",
            "英语水平",
            "毕业时间",
            "工作时间",
            "工作内容",
            "职务",
            "工作单位",
        ]
        # 装载定制模型
        self.ie_custom = None
        # 装载默认模型
        self.ie_default = None

    # 从docx中提取文本
    def get_paragraphs_text_doc(self, path):
        # 打开docx文件
        document = ZipFile(path)
        xml = document.read("word/document.xml")
        wordObj = BeautifulSoup(xml.decode("utf-8"), "lxml")
        # 找到所有的<w:t>、<w:br/>和<w:p>标签，这些标签包含了文字内容、换行符和段落符号
        text_tags = wordObj.find_all(["w:t", "w:p"])
        # 保存提取的文字
        extracted_text = ""
        # 遍历每个标签
        for tag in text_tags:
            # 如果是<w:t>标签，提取文字内容
            if tag.name == "w:t":
                text = tag.text.strip()
                text = text.replace(" ", "")
                if text:
                    extracted_text += text
            # 如果是<w:p>标签，添加段落符号（仅在非空行时添加）
            elif tag.name == "w:p":
                if extracted_text and extracted_text[-1] != "\n":
                    extracted_text += "\n"

        lines = extracted_text.split("\n")
        my_ordered_set = OrderedSet(lines)
        # 输出提取的文字
        newtext = ";".join(my_ordered_set)
        return newtext

    # 从pdf中提取文本
    def get_paragraphs_text_pdf(self, path):
        print(f"path1::{path}")
        images = convert_from_path(
            path, poppler_path="D://Green-Version/poppler-0.68.0/bin"
        )
        # 提取路径
        filename = re.search(r"/([^/]*)\.pdf$", path).group(1)
        prepath = re.match(r"^(.*)/[^/]*?$", path).group(1)
        print(f"path2::{prepath}     {filename}")
        for i in range(len(images)):
            # 将每一页pdf转换为图片
            images[i].save(prepath + f"/{filename}_{i + 1}.png", "PNG")
        self.deleteFile(path)
        return self.get_paragraphs_text_png(path, len(images))

    # 从png中提取文本
    def get_paragraphs_text_png(self, path, count):
        print(f"path3::{path}")
        filename = re.search(r"/([^/]*)\.pdf$", path).group(1)
        # 提取路径
        prepath = re.match(r"^(.*)/[^/]*?$", path).group(1)
        img_files = [prepath + f"/{filename}_{i}.png" for i in range(1, count + 1)]
        # print(img_files)
        for img_file in img_files:
            self.request_webimage(img_file)
            self.deleteFile(img_file)
        text = self.get_paragraphs_text_json(f"{prepath}/{filename}.json")
        return text

    # 调用百度API进行ocr识别
    def request_webimage(self, path):
        filename = re.search(r"/([^/]*)_.*\.png$", path).group(1)
        print(f"path4::{path}")
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        access_token = (
            "your token" # token
        )
        request_url = request_url + "?access_token=" + access_token
        headers = {"content-type": "application/x-www-form-urlencoded"}
        try:
            with open(path, "rb") as f:
                img = base64.b64encode(f.read())
            params = {"image": img}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                print("图片识别结果：", end=" ")
                print(response.json())
                path = re.match(r"^(.*)/[^/]*?$", path).group(1)
                # 将文本写入文件
                filename = path + f"/{filename}.json"
                if not os.path.exists(filename):
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(json.dumps([response.json()]))
                else:
                    with open(filename, "r+", encoding="utf-8") as f:
                        f.seek(0, 2)  # 将文件指针移动到文件末尾
                        print(f.tell())
                        f.seek(f.tell() - 1)
                        f.write(", \n" + json.dumps(response.json()) + "]")
        except ValueError as e:
            print(e)

    # 从json中提取文本
    def get_paragraphs_text_json(self, path):
        print(f"path5::{path}")
        # 读取文件中的JSON数据
        with open(path, encoding="utf-8") as f:
            json_data = f.read()
        # 解析JSON数据
        datas = json.loads(json_data)
        text1 = ""
        for data in datas:
            words_info = data["words_result"]
            for word_info in words_info:
                text1 += word_info["words"] + " "
        self.deleteFile(path)
        print("提取文本：", end=" ")
        print(text1)
        return text1

    # 从txt中提取文本
    def get_paragraphs_text_txt(self, path):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        return text

    # 计算工作年份
    def calculate_work_years(work_periods):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        total_months = 0
        for period in work_periods:
            # 替换可能的分隔符为统一的格式
            period = period.replace("-", "～")
            # 处理“至今”情况
            period = period.replace("至今", f"{current_year}.{current_month}")
            # 提取开始和结束的年份和月份
            match = re.match(
                r"(\d{4})(?:\.(\d{1,2}))?～(\d{4})(?:\.(\d{1,2}))?", period
            )
            if match:
                start_year, start_month, end_year, end_month = match.groups()
                start_year, end_year = int(start_year), int(end_year)
                start_month = int(start_month) if start_month else 1
                end_month = int(end_month) if end_month else 12
                # 计算工作月数
                months = (end_year - start_year) * 12 + end_month - start_month + 1
                total_months += months
        # 计算工作年限，向上取整
        work_years = math.ceil(total_months / 12)
        return work_years

    def get_info1(self, paragraphs_text):
        prompt = f"""你现在的任务是从OCR文字识别的简历结果中提取我指定的关键信息。OCR的文字识别结果使用```符号包围，包含所识别出来的文字，顺序在原始图片中从左至右、从上至下。我指定的关键信息使用[]符号包围。请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、对应错位等问题，你需要结合上下文语义进行综合判断，以抽取准确的关键信息。在返回结果时使用json格式，包含一个key-value对，key值为我指定的关键信息，value值为所抽取的结果（字符串类型）。如果认为OCR识别结果中没有关键信息key，请尝试推断value的值或者赋值为空，不要遗漏key。 请只输出json格式的结果，不要包含其它多余文字！下面正式开始：
        OCR文字：```{paragraphs_text}```
        要抽取的关键信息：[{self.schema}]。"""
        client = ZhipuAI(
            api_key="your apikey" # APIKey
        )  
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        res = response.choices[0].message.content
        print("ChatGLM结果：", end=" ")
        print(res)
        res_stripped = re.search(r"(?<=```json)(.*?)(?=```)", res, re.DOTALL).group(1)
        json_data = json.loads(res_stripped)
        return json_data

    # 提取信息，结合默认模型与微调模型
    def get_info(self, paragraphs_text):
        s = OrderedSet()
        # 创建一个空字典，用于存放抽取结果
        schema_dict = {}
        # 使用微调后的模型抽取信息
        a = self.ie_custom(paragraphs_text)
        # 使用微调前的模型抽取信息
        b = self.ie_default(paragraphs_text)
        # 遍历预定义的schema
        try:
            for i in self.schema:
                if i in a[0]:
                    if i == "性别":  # 如果当前字段是性别
                        # 如果预测结果是男或女，则直接使用该结果
                        if a[0][i][0]["text"] in ["男", "女"]:
                            schema_dict[i] = a[0][i][0]["text"]
                        # 如果微调后的模型预测结果不是男或女，但微调前的模型预测结果是男或女，则使用微调前的模型的预测结果
                        elif i in b[0] and b[0][i][0]["text"] in ["男", "女"]:
                            schema_dict[i] = b[0][i][0]["text"]
                        else:  # 如果两个模型的预测结果都不是男或女，则该字段为空
                            schema_dict[i] = ""
                    elif i == "年龄":  # 如果当前字段是年龄
                        if re.sub(r"\D", "", a[0][i][0]["text"]):
                            # 将非数字的字符替换为空
                            text1 = re.sub(r"\D", "", a[0][i][0]["text"])
                            # 如果字符串长度小于等于 2 ，截取两位，否则截取四位
                            if len(text1) <= 2:
                                result = text1[:2]
                                schema_dict[i] = result
                            elif len(text1) > 2:
                                result = text1[:4]
                                schema_dict[i] = str(2023 - int(result) + 1)
                    elif i == "工作年限":
                        try:
                            for work_period in a[0][i]:
                                s.add(work_period["text"])
                            schema_dict[i] = self.calculate_work_years(s)
                        except Exception as e:
                            schema_dict[i] = "0"
                    else:  # 如果当前字段不是性别也不是年龄，则直接使用微调后的模型的预测结果
                        schema_dict[i] = a[0][i][0]["text"]
                else:  # 如果微调后的模型无法识别当前字段
                    if i in b[0]:  # 如果微调前的模型能识别当前字段
                        if i == "性别":  # 如果当前字段是性别
                            # 如果预测结果是男或女，则直接使用该结果
                            if b[0][i][0]["text"] in ["男", "女"]:
                                schema_dict[i] = b[0][i][0]["text"]
                            else:  # 如果预测结果不是男或或者女，则该字段为空
                                schema_dict[i] = ""
                        elif i == "年龄":  # 如果当前字段是年龄
                            if re.sub(r"\D", "", b[0][i][0]["text"]):
                                # 将非数字的字符替换为空
                                text1 = re.sub(r"\D", "", b[0][i][0]["text"])
                                # 如果字符串长度小于等于 2 ，截取两位，否则截取四位
                                if len(text1) <= 2:
                                    result = text1[:2]
                                    schema_dict[i] = result
                                elif len(text1) > 2:
                                    result = text1[:4]
                                    schema_dict[i] = str(2023 - int(result) + 1)
                        elif i == "工作年限":
                            try:
                                for work_period in b[0][i]:
                                    s.add(work_period["text"])
                                schema_dict[i] = self.calculate_work_years(s)
                            except Exception:
                                schema_dict[i] = "0"
                        else:  # 如果当前字段不是性别也不是年龄，则直接使用微调前的模型的预测结果
                            schema_dict[i] = b[0][i][0]["text"]
                    else:  # 如果微调前的模型也无法识别当前字段，则该字段为空
                        schema_dict[i] = ""
        except TypeError:
            text1 = ""
        print("实体识别结果：", end=" ")
        print(schema_dict)
        return schema_dict

    # 提取文字，根据不同类型进行不同的提取
    def get_word(self, path, flag):
        filenames = os.listdir(path)
        result = []
        for filename in tqdm(filenames):
            full_path = path + "/" + filename
            print(f"full_path::{full_path}")
            if (
                flag == 1 and os.path.isfile(full_path) and filename.endswith(".docx")
            ):  # 添加对文件后缀的检查
                try:
                    paragraphs_text = self.get_paragraphs_text_doc(full_path)
                    # print(paragraphs_text)
                    res = self.get_info(paragraphs_text)
                    res["filename"] = filename
                    result.append(res)
                    self.deleteFile(full_path)
                except Exception as e:  # 捕获所有异常
                    print(f"处理文件 {filename} 时发生错误: {e}")
            elif (
                flag == 2 and os.path.isfile(full_path) and filename.endswith(".pdf")
            ):  # 添加对文件后缀的检查
                try:
                    paragraphs_text = self.get_paragraphs_text_pdf(full_path)
                    # print(paragraphs_text)
                    res = self.get_info(paragraphs_text)
                    res["filename"] = filename
                    result.append(res)
                except Exception as e:  # 捕获所有异常
                    print(f"处理文件 {filename} 时发生错误: {e}")
            elif (
                flag == 3 and os.path.isfile(full_path) and filename.endswith(".png")
            ):  # 添加对文件后缀的检查
                try:
                    paragraphs_text = self.get_paragraphs_text_png(full_path, 1)
                    # print(paragraphs_text)
                    res = self.get_info(paragraphs_text)
                    res["filename"] = filename
                    result.append(res)
                except Exception as e:  # 捕获所有异常
                    print(f"处理文件 {filename} 时发生错误: {e}")
            elif (
                flag == 4 and os.path.isfile(full_path) and filename.endswith(".txt")
            ):  # 添加对文件后缀的检查
                try:
                    paragraphs_text = self.get_paragraphs_text_txt(full_path)
                    # print(paragraphs_text)
                    res = self.get_info(paragraphs_text)
                    res["filename"] = filename
                    result.append(res)
                except Exception as e:  # 捕获所有异常
                    print(f"处理文件 {filename} 时发生错误: {e}")
        return result

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            print(path + " 删除成功！")
        else:
            print()

    def process_result(self, result):
        if result["出生年月"] and not result["年龄"]:
            result["年龄"] = str(2024 - int(result["出生年月"][:4]))
        if not result["年龄"]:
            result["年龄"] = str(25)
        if not result["政治面貌"]:
            result["政治面貌"] = "群众"
        if result["最高学历"]:
            if "学士" in result["最高学历"] or "本科" in result["最高学历"]:
                result["最高学历"] = "本科"
            elif "硕士" in result["最高学历"] or "研究生" in result["最高学历"]:
                result["最高学历"] = "硕士"
        if result["毕业院校"] and not result["最高学历"]:
            if "大学" in result["毕业院校"]:
                result["最高学历"] = "本科"
            elif (
                "职业" in result["毕业院校"]
                or "专科" in result["毕业院校"]
                or "技术" in result["毕业院校"]
            ):
                result["最高学历"] = "大专"
            elif "学院" in result["毕业院校"]:
                result["最高学历"] = "本科"
            else:
                result["最高学历"] = "高中"
        if not result["最高学历"]:
            result["最高学历"] = "高中"
        if result["年龄"] and result["最高学历"]:
            age = int(result["年龄"])
            if result["最高学历"] == "本科":
                result["工作年限"] = str(
                    random.randrange(max(0, age - 25), max(1, age - 22))
                )
            elif "专" in result["最高学历"]:
                result["工作年限"] = str(
                    random.randrange(max(0, age - 23), max(1, age - 19))
                )
            elif "硕" in result["最高学历"]:
                result["工作年限"] = max(0, age - 26)
        if not result["工作年限"]:
            result["工作年限"] = str(
                random.randrange(max(0, age - 23), max(1, age - 20))
            )
        if (
            "硕" in result["最高学历"]
            or "本" in result["最高学历"]
            or "博" in result["最高学历"]
        ):
            if random.randrange(0, 2) == 0:
                result["标签1"] = "博学多才"
            else:
                result["标签1"] = "学历水平高"
        else:
            result["标签1"] = "技能水平高"
        if int(result["工作年限"]) >= 5:
            if random.randrange(0, 2) == 0:
                result["标签2"] = "经验丰富"
            else:
                result["标签2"] = "工作稳定"
        else:
            result["标签2"] = "变动频繁"
        if "英语" in result:
            result["标签3"] = "英语能力良好"
        if (
            "硕" in result["最高学历"]
            or "博" in result["最高学历"]
            or int(result["工作年限"]) >= 10
        ):
            result["预计薪酬"] = "10000-15000元/月"
        elif "本" in result["最高学历"] or int(result["工作年限"]) >= 5:
            result["预计薪酬"] = "7000-10000元/月"
        else:
            result["预计薪酬"] = "4000-6000元/月"
        if "市场" in result["职务"]:
            result["匹配岗位"] = "市场营销"
        elif "设计" in result["职务"]:
            result["匹配岗位"] = "平面设计师"
        elif "经理" in result["职务"]:
            result["匹配岗位"] = "项目主管"
        elif "产品" in result["职务"] or "运营" in result["职务"]:
            result["匹配岗位"] = "产品运营"
        elif "财" in result["职务"] or "会计" in result["职务"]:
            result["匹配岗位"] = "财务"
        if "匹配岗位" in result:
            if (
                "硕" in result["最高学历"]
                or "博" in result["最高学历"]
                or int(result["工作年限"]) >= 10
            ):
                result["优先级"] = "优先级：高"
            elif "本" in result["最高学历"] or int(result["工作年限"]) >= 5:
                result["优先级"] = "优先级：一般"
            else:
                result["优先级"] = "优先级：低"
        print("最终处理结果：", end=" ")
        print(result)
        return result

    # 根据路径解析文件
    def prase(self, path):
        self._path = path
        print(self._path)
        suffix = re.search(r"\.(\w+)$", self._path).group(1)
        if suffix == "docx":
            flag = 1
        elif suffix == "pdf":
            flag = 2
        elif suffix == "png":
            flag = 3
        elif suffix == "txt":
            flag = 4
        else:
            print("不支持的文件类型！")
            self.deleteFile(self._path)
            self.resumeFiled.emit("不支持的文件类型！")
            self.finished.emit()
            return

        # 设置微调模型
        self.ie_custom = Taskflow(
            "information_extraction", schema=self.schema, task_path="model"
        )
        # 设置默认模型
        self.ie_default = Taskflow("information_extraction", schema=self.schema)
        prepath = re.match(r"^(.*)/[^/]*?$", self._path).group(1)
        result = self.get_word(prepath, flag)
        if result:
            self.resumeParsed.emit(self.process_result(result[0]))
        else:
            self.resumeFiled.emit("解析失败！")
            print("解析失败！")
        self.finished.emit()

    # 根据文字解析
    def prase2(self, text):
        # 设置微调模型
        self.ie_custom = Taskflow(
            "information_extraction", schema=self.schema, task_path="model"
        )
        # 设置默认模型
        self.ie_default = Taskflow("information_extraction", schema=self.schema)
        result = []
        try:
            res = self.get_info(text)
            res["filename"] = "tmp.txt"
            result.append(res)
        except Exception as e:  # 捕获所有异常
            print(f"处理文字发生错误: {e}")
        if result:
            self.resumeParsed.emit(self.process_result(result[0]))
        else:
            self.resumeFiled.emit("解析失败！")
            print("解析失败！")
        self.finished.emit()

    def resume_visiual(self):
        time.sleep(5)
        # 读取Excel表格数据
        data = pandas.read_excel("测试集.xlsx")
        self.resumeVisiualParsed.emit(data)
        self.finished.emit()
