# Bing 壁紙

[![Update Bing Wallpaper](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml/badge.svg?event=schedule)](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml)

[[🇩🇪 Deutsch ドイツ語](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English 英語](README_en.md)] [[🇪🇸 Español スペイン語](README_es.md)] [[🇨🇦 🇫🇷 Français フランス語](README_fr.md)] [[🇮🇹 Italiano イタリア語](README_it.md)] [[🇧🇷 Português ポルトガル語](README_pt.md)] [[🇨🇳 中文 中国語](README.md)]

## リージョンリスト

| リージョンコード | タイムゾーン                                     | 備考                                               |
| :--------------: | :----------------------------------------------- | :------------------------------------------------- |
|     `de-DE`      | [`Europe/Berlin`](https://time.is/Germany)       |                                                    |
|     `en-CA`      | [`America/Toronto`](https://time.is/Canada)      |                                                    |
|     `en-GB`      | [`Europe/London`](https://time.is/England)       |                                                    |
|     `en-IN`      | [`Asia/Kolkata`](https://time.is/India)          | `hi-IN` はこれとほぼ同じであり、同様に除外されます |
|     `en-US`      | [`America/Los_Angeles`](https://time.is/Redmond) |                                                    |
|     `es-ES`      | [`Europe/Madrid`](https://time.is/Spain)         |                                                    |
|     `fr-CA`      | [`America/Toronto`](https://time.is/Canada)      |                                                    |
|     `fr-FR`      | [`Europe/Paris`](https://time.is/France)         |                                                    |
|     `it-IT`      | [`Europe/Rome`](https://time.is/Italy)           |                                                    |
|     `ja-JP`      | [`Asia/Tokyo`](https://time.is/Japan)            |                                                    |
|     `pt-BR`      | [`America/Sao_Paulo`](https://time.is/Brazil)    |                                                    |
|     `zh-CN`      | [`Asia/Shanghai`](https://time.is/China)         |                                                    |

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
        ), // 一部の地域では、このパターンにマッチしないデータが存在することがわかっています
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // 一部の地域では、このパターンにマッチしないデータが存在することがわかっています
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // 一部の地域では、このパターンにマッチしないデータが存在することがわかっています
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          )
          .or(z.literal("")),
        Link: z
          .string()
          .startsWith("https://www.bing.com/maps?")
          .or(z.literal("")),
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

本プロジェクトではデータ保存に jsonl を採用しています。各ロケールのデータは `data` フォルダ内の対応するファイルに保存されます。各行が 1 日分の壁紙を表し、各日の壁紙には以下のフィールドがあります：

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

## 類似プロジェクト

- <https://wallpaper.bokewo.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-CA`、`fr-FR`、`ja-JP`、`zh-CN`)
- <https://dailybing.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://github.com/zkeq/Bing-Wallpaper-Action/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
- <https://bing.gifposter.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://peapix.com/bing/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://bingwallpaper.anerg.com/> (`de-DE`、`en-CA`、`en-GB`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
