"""实用工具"""

import json
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import pytz

# 区域代码与时区映射
REGION_TIMEZONES = {
    "de-DE": "Europe/Berlin",
    "en-CA": "America/Toronto",
    "en-GB": "Europe/London",
    "en-IN": "Asia/Kolkata",
    "en-US": "America/Los_Angeles",
    "es-ES": "Europe/Madrid",
    "fr-CA": "America/Toronto",
    "fr-FR": "Europe/Paris",
    "it-IT": "Europe/Rome",
    "ja-JP": "Asia/Tokyo",
    "pt-BR": "America/Sao_Paulo",
    "zh-CN": "Asia/Shanghai",
}


class BingDataEntryApp:
    """Bing 每日图片数据生成器 GUI 应用程序"""

    def __init__(self, root):
        self.root = root
        root.title("Bing 每日图片数据生成器")
        root.geometry("700x700")

        # 创建输入字段
        self.create_widgets()

        # 设置默认值
        self.region_var.set("de-DE")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.update_full_start_time()

    def create_widgets(self):
        """创建 GUI 输入字段和按钮"""
        # 创建区域选择单选按钮组
        ttk.Label(self.root, text="区域代码：").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )

        # 创建框架容器用于放置单选按钮
        region_frame = ttk.Frame(self.root)
        region_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.region_var = tk.StringVar()
        regions = list(REGION_TIMEZONES.keys())

        # 每行放置 6 个单选按钮
        for i, region in enumerate(regions):
            row = i // 6
            col = i % 6
            rb = ttk.Radiobutton(
                region_frame,
                text=region,
                variable=self.region_var,
                value=region,
                command=self.update_full_start_time,
            )
            rb.grid(row=row, column=col, padx=5, pady=2, sticky="w")

        # 设置默认选择
        self.region_var.set("de-DE")

        # 日期输入
        ttk.Label(self.root, text="日期 (YYYY-MM-DD):").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(self.root, textvariable=self.date_var, width=15)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.date_entry.bind("<KeyRelease>", lambda e: self.update_full_start_time())

        # full_start_time 显示
        ttk.Label(self.root, text="full_start_time (UTC):").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.full_start_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.full_start_var).grid(
            row=2, column=1, padx=10, pady=5, sticky="w"
        )

        # image_url 输入
        ttk.Label(self.root, text="image_url 标识符：").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.image_id_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.image_id_var, width=40).grid(
            row=3, column=1, padx=10, pady=5, sticky="we"
        )

        # copyright 输入
        ttk.Label(self.root, text="copyright (以©开头):").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.copyright_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.copyright_var, width=40).grid(
            row=4, column=1, padx=10, pady=5, sticky="we"
        )

        # search_url 搜索词
        ttk.Label(self.root, text="search_url 搜索词：").grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )
        self.search_term_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.search_term_var, width=40).grid(
            row=5, column=1, padx=10, pady=5, sticky="we"
        )

        # title 输入
        ttk.Label(self.root, text="title:").grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )
        self.title_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.title_var, width=40).grid(
            row=6, column=1, padx=10, pady=5, sticky="we"
        )

        # description 输入
        ttk.Label(self.root, text="description:").grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )
        self.description_text = tk.Text(self.root, height=5, width=50)
        self.description_text.grid(row=7, column=1, padx=10, pady=5, sticky="we")

        # headline 输入
        ttk.Label(self.root, text="headline:").grid(
            row=8, column=0, padx=10, pady=5, sticky="w"
        )
        self.headline_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.headline_var, width=40).grid(
            row=8, column=1, padx=10, pady=5, sticky="we"
        )

        # 按钮
        ttk.Button(self.root, text="生成 JSON 数据", command=self.generate_json).grid(
            row=9, column=1, padx=10, pady=20, sticky="e"
        )

        # 结果显示
        ttk.Label(self.root, text="生成的 JSON:").grid(
            row=10, column=0, padx=10, pady=5, sticky="nw"
        )
        self.result_text = tk.Text(self.root, height=10, width=80)
        self.result_text.grid(row=10, column=1, padx=10, pady=5, sticky="we")

        # 配置网格权重
        self.root.columnconfigure(1, weight=1)

    def update_full_start_time(self):
        """根据区域和日期更新 full_start_time: 输入日期在所在时区的 0 点对应的 UTC 时间"""
        try:
            region = self.region_var.get()
            date_str = self.date_var.get()

            # 获取区域对应的时区
            timezone_str = REGION_TIMEZONES.get(region)
            if not timezone_str:
                self.full_start_var.set("无效区域代码")
                return

            # 创建区域时区对象
            tz = pytz.timezone(timezone_str)

            # 解析输入日期（在区域时区）
            local_date = datetime.strptime(date_str, "%Y-%m-%d")

            # 获取该日期在区域时区的 0 点
            local_start = tz.localize(local_date)

            # 转换为 UTC 时间
            utc_start = local_start.astimezone(pytz.UTC)

            # 格式化为 ISO 字符串并设置
            self.full_start_var.set(utc_start.strftime("%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            self.full_start_var.set("无效日期格式")
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.full_start_var.set(f"错误：{str(e)}")

    def generate_json(self):
        """生成 JSON 数据并显示在结果框中"""
        try:
            # 获取基本字段
            region = self.region_var.get()
            date = self.date_var.get()
            full_start = self.full_start_var.get()
            image_id = self.image_id_var.get()
            copyright_text = self.copyright_var.get()
            search_term = self.search_term_var.get()
            title = self.title_var.get()
            description = self.description_text.get("1.0", tk.END).strip()
            headline = self.headline_var.get()

            # 验证必要字段
            if not all(
                [
                    region,
                    date,
                    image_id,
                    copyright_text,
                    search_term,
                    title,
                    description,
                    headline,
                ]
            ):
                messagebox.showerror("错误", "请填写所有必填字段")
                return

            # 处理 image_url
            image_url = f"https://www.bing.com/th?id=OHR.{image_id}_UHD.jpg"

            # 处理 search_url
            date_part = full_start.replace("-", "").replace(":", "").split("T")[0]
            time_part = full_start.replace(":", "").split("T")[1][:4]
            search_url = (
                f"https://www.bing.com/search?q={search_term}&form=BGALM"
                f'&filters=HpDate:"{date_part}_{time_part}"'
            )

            # 处理 quiz_url
            image_key = image_id.split("_")[0]  # 获取第一个下划线前的部分
            quiz_date = date.replace("-", "")
            quiz_url = (
                "https://www.bing.com/search?q=Bing+homepage+quiz&filters="
                f'WQOskey:"HPQuiz_{quiz_date}_{image_key}"&FORM=BGAQ'
            )

            # 构建 JSON 对象
            data = {
                "date": date,
                "full_start_time": full_start,
                "image_url": image_url,
                "copyright": copyright_text,
                "search_url": search_url,
                "title": title,
                "description": description,
                "headline": headline,
                "quiz_url": quiz_url,
                "map_image": "",
                "map_url": "",
            }

            # 显示在结果框
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", json.dumps(data, ensure_ascii=False))

        except Exception as e:  # pylint: disable=broad-exception-caught
            messagebox.showerror("错误", f"生成数据时出错：{str(e)}")


if __name__ == "__main__":
    app_root = tk.Tk()
    app = BingDataEntryApp(app_root)
    app_root.mainloop()
