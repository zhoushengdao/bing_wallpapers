# Bing 壁紙

[[🇩🇪 Deutsch ドイツ語](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English 英語](README_en.md)] [[🇪🇸 Español スペイン語](README_es.md)] [[🇨🇦 🇫🇷 Français フランス語](README_fr.md)] [[🇮🇹 Italiano イタリア語](README_it.md)] [[🇧🇷 Português ポルトガル語](README_pt.md)] [[🇨🇳 中文 中国語](README.md)]

## リージョンリスト

| リージョンコード | タイムゾーン                                                      | 備考                                               |
| :--------------: | :---------------------------------------------------------------- | :------------------------------------------------- |
|     `de-DE`      | 標準時：`UTC+1`，夏時間：`UTC+2`，[出典](https://time.is/Germany) |                                                    |
|     `en-CA`      | 標準時：`UTC-5`，夏時間：`UTC-4`，[出典](https://time.is/Canada)  |                                                    |
|     `en-GB`      | 標準時：`UTC+0`，夏時間：`UTC+1`，[出典](https://time.is/England) |                                                    |
|     `en-IN`      | `UTC+5:30`，[出典](https://time.is/India)                         | `hi-IN` はこれとほぼ同じであり、同様に除外されます |
|     `en-US`      | 標準時：`UTC-8`，夏時間：`UTC-7`，[出典](https://time.is/Redmond) |                                                    |
|     `es-ES`      | 標準時：`UTC+1`，夏時間：`UTC+2`，[出典](https://time.is/Spain)   |                                                    |
|     `fr-CA`      | 標準時：`UTC-5`，夏時間：`UTC-4`，[出典](https://time.is/Canada)  |                                                    |
|     `fr-FR`      | 標準時：`UTC+1`，夏時間：`UTC+2`，[出典](https://time.is/France)  |                                                    |
|     `it-IT`      | 標準時：`UTC+1`，夏時間：`UTC+2`，[出典](https://time.is/Italy)   |                                                    |
|     `ja-JP`      | `UTC+9`，[出典](https://time.is/Japan)                            |                                                    |
|     `pt-BR`      | `UTC-3`，[出典](https://time.is/Brazil)                           |                                                    |
|     `zh-CN`      | `UTC+8`，[出典](https://time.is/China)                            |                                                    |

詳細は [regional_list.csv](regional_list.csv) をご覧ください

## データソース

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

返されるデータ構造は [zod](https://zod.dev/) で以下のように表現されます。

```javascript
z.object({
  images: z.array(
    z.object({
      startdate: z.string().regex(/^\d{8}$/),
      fullstartdate: z.string().regex(/^\d{12}$/),
      enddate: z.string().regex(/^\d{8}$/),
      urlbase: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/th\?id=OHR\.([A-Za-z0-9]+)_(DE-DE|EN-CA|EN-GB|EN-IN|EN-US|ES-ES|FR-CA|FR-FR|IT-IT|JA-JP|PT-BR|ZH-CN)(\d+)_UHD\.jpg$/
        ), // en-GB ロケールにこのスキーマに適合しないデータが存在することが知られています
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // en-GB ロケールにこのスキーマに適合しないデータが存在することが知られています
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // en-GB ロケールにこのスキーマに適合しないデータが存在することが知られています
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          ),
        Link: z.string().startsWith("https://www.bing.com/maps?"),
      }),
      quizId: z.null(), // null 以外の値は見つかりませんでした
      fullDateString: z.string(), // 現地言語での現地日付
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // 通常は空文字列
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // 通常は false
      CTAData: z.null(), // null 以外の値は見つかりませんでした
      detectedRegion: z.string(), // リクエストを送信する地域によって異なります
      enableBingImageCreator: z.boolean(), // 通常は false
      topRightCTAData: z.looseObject({}), // 重要でないデータ
      imageHotspots: z.null(), // null 以外の値は見つかりませんでした
      AnimatedWP: z.null(), // null 以外の値は見つかりませんでした
    })
  ),
  tooltips: z.looseObject({}), // 重要でないデータ
  imageCount: z.literal(8),
});
```

## フィールドリスト

| フィールド名      | ソース                                                                              | 備考                       |
| :---------------- | :---------------------------------------------------------------------------------- | :------------------------- |
| `date`            | `images[].fullstartdate` にタイムゾーンオフセット（上記参照）を追加して得られる日付 | 日付部分のみ               |
| `full_start_time` | `images[].fullstartdate`                                                            | UTC 時間、時間単位まで正確 |
| `image_url`       | `images[].urlbase`                                                                  | 注 1 を参照                |
| `copyright`       | `images[].copyrighttext`                                                            |                            |
| `search_url`      | `images[].copyrightlink`                                                            |                            |
| `title`           | `images[].title`                                                                    |                            |
| `description`     | `images[].description`                                                              |                            |
| `headline`        | `images[].headline`                                                                 |                            |
| `quiz_url`        | `images[].quiz`                                                                     |                            |
| `map_image`       | `images[].mapLink.Url`                                                              | 注 2 を参照                |
| `map_url`         | `images[].mapLink.Link`                                                             | 注 2 を参照                |

1. `image_url` はデフォルトで横長の 4K 画像（3840x2160）を返します。パラメータ `&w=<幅>&h=<高さ>&rs=1&c=4` を追加することで画像をトリミングできますが、画像の最大サイズを超えないように注意してください。
2. `map_image` と `map_url` は現在、以下の地域の一部画像でのみ提供されています：`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`fr-CA`、`fr-FR`、`it-IT`、`ja-JP`。
