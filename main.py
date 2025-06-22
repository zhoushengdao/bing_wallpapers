"""必应壁纸"""

# TODO 添加错误处理和日志记录

from pathlib import Path
from datetime import datetime
from collections import OrderedDict
from re import match

from requests import get
from pytz import utc, timezone as tz
from jsonlines import open as jsonl_open

API_BASE = "https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt="

LOCALES = OrderedDict(
    [
        ("de-DE", "Europe/Berlin"),
        ("en-CA", "America/Toronto"),
        ("en-GB", "Europe/London"),
        ("en-IN", "Asia/Kolkata"),
        ("en-US", "America/Los_Angeles"),
        ("es-ES", "Europe/Madrid"),
        ("fr-CA", "America/Toronto"),
        ("fr-FR", "Europe/Paris"),
        ("it-IT", "Europe/Rome"),
        ("ja-JP", "Asia/Tokyo"),
        ("pt-BR", "America/Sao_Paulo"),
        ("zh-CN", "Asia/Shanghai"),
    ]
)

DATA_DIR = Path.cwd() / "data"
ARCHIVE_DIR = Path.cwd() / "archive"


def is_data_valid(data):
    """检查数据是否有效"""
    if not (
        isinstance(data.get("image_url"), str)
        and match(
            r"^https://www\.bing\.com/th\?id=OHR\.([A-Za-z0-9]+)_(DE-DE|EN-CA|EN-GB|"
            r"EN-IN|EN-US|ES-ES|FR-CA|FR-FR|IT-IT|JA-JP|PT-BR|ZH-CN)(\d+)_UHD\.jpg$",
            data["image_url"],
        )
    ):
        return False

    if not (
        isinstance(data.get("copyright"), str) and data["copyright"].startswith("© ")
    ):
        return False

    if not (
        isinstance(data.get("search_url"), str)
        and match(
            r"^https://www\.bing\.com/search\?q=([^&]+)&form="
            r"BGALM(?:&filters=HpDate:\"(\d{8}_\d{4})\")$",
            data["search_url"],
        )
    ):
        return False

    if not (
        isinstance(data.get("quiz_url"), str)
        and match(
            r"^https://www\.bing\.com/search\?q=Bing\+homepage\+quiz"
            r"&filters=WQOskey:\"HPQuiz_(\d{8})_([^\"]+)\"&FORM=BGAQ$",
            data["quiz_url"],
        )
    ):
        return False

    if not (
        isinstance(data.get("map_image"), str)
        and data["map_image"].startswith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
        )
    ):
        return False

    if not (
        isinstance(data.get("map_url"), str)
        and data["map_url"].startswith("https://www.bing.com/maps?")
    ):
        return False

    # 所有验证通过
    return True


def is_different(origin_data, current_data):
    """检查数据是否发生变化"""
    for key in [
        "image_url",
        "copyright",
        "search_url",
        "title",
        "description",
        "headline",
        "quiz_url",
        "map_image",
        "map_url",
    ]:
        if origin_data[key] != current_data[key]:
            return True
    return False


def get_image_data(locale, data):
    """将原始数据格式转换为目标格式"""

    # * ValueError
    utc_time = utc.localize(
        datetime.strptime(data.get("fullstartdate", ""), "%Y%m%d%H%M")
    )
    date = utc_time.astimezone(tz(LOCALES[locale])).strftime("%Y-%m-%d")
    map_link_obj = data.get("mapLink", {})

    result = {
        "date": date,
        "full_start_time": utc_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "image_url": data.get("urlbase", ""),
        "copyright": data.get("copyrighttext", ""),
        "search_url": data.get("copyrightlink", ""),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "headline": data.get("headline", ""),
        "quiz_url": data.get("quiz", ""),
        "map_image": map_link_obj.get("Url", ""),
        "map_url": map_link_obj.get("Link", ""),
    }

    return (date, result)


def get_data_file_path(locale, backup=False) -> Path:
    """获取数据文件路径"""
    backup_suffix = f"_{datetime.now().strftime("%Y%m%d_%H%M%S")}" if backup else ""
    file_path = DATA_DIR / f"{locale}{backup_suffix}.jsonl"
    if (not file_path.exists()) and (not backup):
        file_path.touch()
    return file_path


def get_locale(locale):
    """获取指定区域的壁纸数据"""
    file_path = get_data_file_path(locale)
    backup_file_path = get_data_file_path(locale, backup=True)

    res = get(f"{API_BASE}{locale}", timeout=60)
    print(f"{locale} {res.status_code}")
    data = res.json()
    if ("images" not in data) or (not isinstance(data["images"], list)):
        raise ValueError(f"Invalid data format for {locale}")

    images = data["images"]
    images_data = OrderedDict()
    for image in images:
        date, image_data = get_image_data(locale, image)
        if is_data_valid(image_data):
            images_data[date] = image_data
        else:
            # TODO
            pass

    file_path.rename(backup_file_path)

    with jsonl_open(backup_file_path, mode="r") as backup_file, jsonl_open(
        file_path, mode="w"
    ) as file:
        for backup_file_data in backup_file.iter(type=dict, skip_invalid=True):
            item_date = backup_file_data["date"]
            if item_date not in images_data:
                file.write(backup_file_data)
            else:
                file.write(images_data[item_date])
                images_data.pop(item_date)
        if len(images_data) > 0:
            for item_date, item_data in reversed(images_data.items()):
                file.write(item_data)

    backup_file_path.rename(ARCHIVE_DIR / backup_file_path.name)


def main():
    """主函数"""
    for locale in LOCALES:
        get_locale(locale)


if __name__ == "__main__":
    main()
