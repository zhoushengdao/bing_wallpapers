"""获取必应图片 API 所有可用的区域列表"""

import csv
import json
import time

import requests

LOCALES_URL = "https://cdn.simplelocalize.io/public/v1/locales"
BING_BASE_URL = "https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt="

try:
    # 获取 locale 数据
    response = requests.get(LOCALES_URL, timeout=10)
    response.raise_for_status()
    locales_data = response.json()

    print(f"\x1b[34m 获取到 {len(locales_data)} 个 locale\x1b[0m")

    # 准备写入 CSV
    with open("bing_images.csv", "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["locale", "timezones", "urlbase", "fullstartdate"])

        # 遍历每个 locale 获取图片数据
        for locale_data in locales_data:
            locale = locale_data.get("locale", "")
            timezones = json.dumps(locale_data.get("country", {}).get("timezones", []))
            try:
                # 请求 Bing 图片 API
                bing_response = requests.get(f"{BING_BASE_URL}{locale}", timeout=15)
                bing_response.raise_for_status()
                bing_data = bing_response.json()

                # 提取第一个图片的 urlbase
                if bing_data.get("images") and len(bing_data["images"]) > 0:
                    urlbase = (
                        bing_data["images"][0]
                        .get("urlbase", "")
                        .replace("https://www.bing.com/th?id=", "")
                    )
                    fullstartdate = bing_data["images"][0].get("fullstartdate", "")
                    csv_writer.writerow([locale, timezones, urlbase, fullstartdate])
                    print(f"\x1b[32m{locale}\x1b[0m", end=" ")
                else:
                    csv_writer.writerow(
                        [locale, timezones, "error: null", "error: null"]
                    )
                    print(f"\x1b[31m{locale}\x1b[0m", end=" ")

            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"\x1b[31m{locale}\x1b[0m", end=" ")
                csv_writer.writerow([locale, timezones, f"error: {e}", f"error: {e}"])

            # 添加延迟避免请求过快
            time.sleep(0.5)

except Exception as e:  # pylint: disable=broad-exception-caught
    print(e)
