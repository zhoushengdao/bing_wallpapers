"""生成错误日志的 Markdown 仪表盘"""

from re import compile as recompile
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from os import getenv


def generate_log_dashboard(input_path: Path, output_path: Path):
    """生成错误日志的 Markdown 仪表盘"""
    # 读取日志文件
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            log_content = file.read()
            log_lines = log_content.splitlines()
    except FileNotFoundError:
        print(f"错误：文件 {input_path} 不存在")
        return

    if not log_lines:
        print("错误日志为空")
        return

    # 解析错误信息
    errors = []
    current_locale = None
    current_date = None

    locale_pattern = recompile(r"\[([a-zA-Z]{2}-[a-zA-Z]{2})\]")
    date_pattern = recompile(r'"date": "(\d{4}-\d{2}-\d{2})"')

    for line in log_lines:
        # 检查区域
        locale_match = locale_pattern.search(line)
        if locale_match:
            current_locale = locale_match.group(1)

        # 检查日期
        date_match = date_pattern.search(line)
        if date_match:
            current_date = date_match.group(1)

        # 记录错误
        if "ERROR" in line and current_locale and current_date:
            errors.append((current_locale, current_date))

    # 统计错误
    error_stats = defaultdict(lambda: defaultdict(int))
    all_dates = set()
    all_locales = set()

    for locale, date in errors:
        error_stats[locale][date] += 1
        all_dates.add(date)
        all_locales.add(locale)

    # 准备日期列
    sorted_dates = sorted(all_dates)

    # 生成错误统计表
    table_lines = []
    table_lines.append("| 区域 ＼ 日期 | " + " | ".join(sorted_dates) + " |")
    table_lines.append("| :---: | " + " | ".join([":---:"] * len(sorted_dates)) + " |")

    for locale in sorted(all_locales):
        row = [f"**{locale}**"]
        for date in sorted_dates:
            count = error_stats[locale].get(date, 0)
            row.append(str(count) if count > 0 else "·")
        table_lines.append("| " + " | ".join(row) + " |")

    error_table = "\n".join(table_lines)

    # 解析区域统计信息
    locale_stats = {}
    summary_pattern = recompile(
        r"\[([a-zA-Z]{2}-[a-zA-Z]{2})\] 完成，保留 (\d+)，更新 (\d+)，新增 (\d+)，总计 (\d+)"
    )

    for line in log_lines:
        match = summary_pattern.search(line)
        if match:
            locale = match.group(1)
            locale_stats[locale] = {
                "keep": int(match.group(2)),
                "update": int(match.group(3)),
                "add": int(match.group(4)),
                "total": int(match.group(5)),
                "errors": sum(error_stats[locale].values()),
            }

    # 生成区域概览表
    overview_lines = []
    overview_lines.append("| 区域 | 错误 | 保留 | 更新 | 新增 | 总计 |")
    overview_lines.append("| :---: | :---: | :---: | :---: | :---: | :---: |")

    for locale, stats in sorted(locale_stats.items()):
        overview_lines.append(
            f"| **{locale}** | {stats['errors']} | {stats['keep']} | "
            f"{stats['update']} | {stats['add']} | {stats['total']} |"
        )

    overview_table = "\n".join(overview_lines)

    # 生成完整 Markdown 内容
    md_content = [
        f"# 自动更新 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC",
        "",
        "[[📜查看持久日志](https://github.com/zhoushengdao/bing_wallpaper/issues/3)] "
        f"[[⬇️下载本次日志]({getenv('LOG_URL')})] "
        f"[[💾下载备份数据]({getenv('BACKUP_URL')})]",
        "",
        "## 区域概览",
        overview_table,
        "",
        "## 分区域和日期的报错统计",
        error_table,
        "",
        "## 原始日志",
        f"```\n{log_content}\n```",
    ]

    # 写入输出文件
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(md_content))

    print(f"仪表盘已生成至：{output_path}")


if __name__ == "__main__":
    input_file = Path(__file__).parent / "log.log"
    output_file = Path(__file__).parent / "issue_body.md"

    generate_log_dashboard(input_file, output_file)
