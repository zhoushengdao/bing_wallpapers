"""生成错误日志的 Markdown 仪表盘"""

from pathlib import Path
from collections import defaultdict
from datetime import datetime

from jsonlines import open as jsonl_open


def generate_error_dashboard(input_path: Path, output_path: Path):
    """生成错误日志的 Markdown 仪表盘"""
    # 读取 JSONL 文件
    data = []
    try:
        with jsonl_open(input_path, "r") as reader:
            for line in reader.iter(type=dict, skip_invalid=True):
                data.append(line)
    except FileNotFoundError:
        print(f"错误：文件 {input_path} 不存在")
        return

    if not data:
        md_content = [
            f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC",
            "- **生成状态**: [![Generate Error Dashboard](https://github.com/zhoushengdao/"
            "bing_wallpaper/actions/workflows/dashboard.yaml/badge.svg?event=schedule)]"
            "(https://github.com/zhoushengdao/bing_wallpaper/actions/workflows/dashboard.yaml)",
            f"- **数据来源**: [`{input_path.name}`]"
            "(https://github.com/zhoushengdao/bing_wallpaper/blob/main/data/.error_log.jsonl)",
            "",
            "## 概览",
            "- **总错误数**: 0",
        ]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))
        print(f"仪表盘已生成至：{output_path}")
        return

    # 基础统计
    unique_locales = sorted({entry["locale"] for entry in data})
    unique_dates = sorted({entry["date"] for entry in data})

    # 按 locale 和 date 统计
    locale_date_counts = defaultdict(lambda: defaultdict(int))
    for entry in data:
        locale = entry["locale"]
        date = entry["date"]
        locale_date_counts[locale][date] += 1

    # 生成 Markdown 内容
    md_content = [
        f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        "- **生成状态**: [![Generate Error Dashboard](https://github.com/zhoushengdao/bing_wallpaper"
        "/actions/workflows/dashboard.yaml/badge.svg?event=schedule)](https://github.com"
        "/zhoushengdao/bing_wallpaper/actions/workflows/dashboard.yaml)",
        f"- **数据来源**: [`{input_path.name}`]"
        "(https://github.com/zhoushengdao/bing_wallpaper/blob/main/data/.error_log.jsonl)",
        "",
        "## 概览",
        f"- **总错误数**: {len(data)}",
        f"- **覆盖日期范围**: {min(unique_dates)} 到 {max(unique_dates)}",
        "",
        "## 按区域和日期统计",
        "| 区域 ＼ 日期 | " + " | ".join(unique_dates) + " |",
        "|--------------|" + ":---:|" * len(unique_dates),
    ]

    # 添加表格行
    for locale in unique_locales:
        row = [f"**{locale}**"]
        for date in unique_dates:
            count = locale_date_counts[locale].get(date, 0)
            row.append(str(count) if count > 0 else "·")
        md_content.append("| " + " | ".join(row) + " |")

    # 写入 Markdown 文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

    print(f"仪表盘已生成至：{output_path}")


if __name__ == "__main__":
    input_file = Path(__file__).parent / "data" / ".error_log.jsonl"
    output_file = Path(__file__).parent / "issue_body.md"

    generate_error_dashboard(input_file, output_file)
