"""必应壁纸"""

import logging
from collections import OrderedDict
from datetime import datetime
from json import dumps
from pathlib import Path
from re import match

from jsonlines import open as jsonl_open
from pytz import timezone as tz
from pytz import utc
from requests import get
from requests.exceptions import RequestException

logging.basicConfig(
    filename="log.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

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
ARCHIVE_DIR.mkdir(exist_ok=True)


def valid_data(data):
    """检查数据是否有效"""
    if not match(
        r"^https://www\.bing\.com/th\?id=OHR\.([A-Za-z0-9]+)_(DE-DE|EN-CA|EN-GB|"
        r"EN-IN|EN-US|ES-ES|FR-CA|FR-FR|IT-IT|JA-JP|PT-BR|ZH-CN)(\d+)_UHD\.jpg$",
        data["image_url"],
    ):
        raise ValueError("image_url 格式不正确")

    if not data["copyright"].startswith("© "):
        raise ValueError("copyright 格式不正确")

    if not match(
        r"^https://www\.bing\.com/search\?q=([^&]+)&form="
        r"BGALM(?:&filters=HpDate:\"(\d{8}_\d{4})\")$",
        data["search_url"],
    ):
        raise ValueError("search_url 格式不正确")

    if not match(
        r"^https://www\.bing\.com/search\?q=Bing\+homepage\+quiz"
        r"&filters=WQOskey:\"HPQuiz_(\d{8})_([^\"]+)\"&FORM=BGAQ$",
        data["quiz_url"],
    ):
        raise ValueError("quiz_url 格式不正确")

    if data["map_image"] and not data["map_image"].startswith(
        "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
    ):
        raise ValueError("map_image 格式不正确")

    if data["map_url"] and not data["map_url"].startswith("https://www.bing.com/maps?"):
        raise ValueError("map_url 格式不正确")


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
        if origin_data.get(key, "") != current_data.get(key, ""):
            return True
    return False


def get_image_data(locale, data):
    """将原始数据格式转换为目标格式"""

    utc_time = utc.localize(
        datetime.strptime(data.get("fullstartdate", ""), "%Y%m%d%H%M")
    )
    date = utc_time.astimezone(tz(LOCALES[locale])).strftime("%Y-%m-%d")
    map_link_obj = data.get("mapLink", {})
    if not isinstance(map_link_obj, dict):
        logger.info("[%s] image_data=%s", locale, dumps(data, indent=2))
        logger.error("[%s] API 返回的 image 数据中 mapLink 不是字典", locale)
        map_link_obj = {}

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
    logger.info("[%s] 开始获取区域数据", locale)
    file_path = get_data_file_path(locale)
    backup_file_path = get_data_file_path(locale, backup=True)

    res = get(f"{API_BASE}{locale}", timeout=60)
    logger.info("[%s] API 返回状态码 %s", locale, res.status_code)
    data = res.json()
    if "images" not in data:
        logger.info("[%s] data=%s", locale, dumps(data, indent=2))
        raise ValueError(f"[{locale}] API 未返回 images 数据")
    if not isinstance(data["images"], list):
        logger.info("[%s] data=%s", locale, dumps(data, indent=2))
        raise ValueError(f"[{locale}] API 返回的 images 数据不是列表")

    images = data["images"]
    images_data = OrderedDict()
    for image in images:
        if not isinstance(image, dict):
            logger.info("[%s] image_data=%s", locale, dumps(image, indent=2))
            logger.error("[%s] API 返回的 images 数据元素不是字典", locale)

        try:
            date, image_data = get_image_data(locale, image)
        except ValueError as error:
            logger.info("[%s] image_data=%s", locale, dumps(image, indent=2))
            logger.error("[%s] %s", locale, error)
            continue

        try:
            valid_data(image_data)
        except (ValueError, KeyError) as error:
            logger.info("[%s] image_data=%s", locale, dumps(image_data, indent=2))
            logger.error("[%s] %s", locale, error)
        else:
            images_data[date] = image_data

    file_path.rename(backup_file_path)

    unchanged_items = 0
    updated_items = 0
    appended_items = 0

    with jsonl_open(backup_file_path, mode="r") as backup_file, jsonl_open(
        file_path, mode="w"
    ) as file:
        for backup_file_data in backup_file.iter(type=dict, skip_invalid=True):
            item_date = backup_file_data["date"]
            if item_date not in images_data:
                file.write(backup_file_data)
                unchanged_items += 1
            else:
                if is_different(backup_file_data, images_data[item_date]):
                    logger.info(
                        "[%s] old_image_data=%s",
                        locale,
                        dumps(backup_file_data, indent=2),
                    )
                    logger.info(
                        "[%s] new_image_data=%s",
                        locale,
                        dumps(images_data[item_date], indent=2),
                    )
                    logger.info("[%s] %s 的数据已更新", locale, item_date)
                    updated_items += 1
                else:
                    unchanged_items += 1
                file.write(images_data[item_date])
                images_data.pop(item_date)
        if len(images_data) > 0:
            for item_date, item_data in reversed(images_data.items()):
                logger.info(
                    "[%s] new_image_data=%s",
                    locale,
                    dumps(item_data, indent=2),
                )
                logger.info("[%s] %s 的数据已新增", locale, item_date)
                appended_items += 1
                file.write(item_data)

    logger.info(
        "[%s] 区域数据处理完成，%s 个数据已保留，%s 个数据已更新，%s 个数据已新增，现共有 %s 个数据",
        locale,
        unchanged_items,
        updated_items,
        appended_items,
        unchanged_items + updated_items + appended_items,
    )

    backup_file_path.rename(ARCHIVE_DIR / backup_file_path.name)


def main():
    """主函数"""
    logger.info("程序启动")
    for locale in LOCALES:
        try:
            get_locale(locale)
        except (ValueError, RequestException) as error:
            logger.error("[%s] %s", locale, error)


if __name__ == "__main__":
    main()
