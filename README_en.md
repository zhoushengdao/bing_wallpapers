# Bing Wallpapers

[![Update Bing Wallpaper](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml/badge.svg?event=schedule)](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml)

[[🇩🇪 Deutsch German](README_de.md)] [[🇪🇸 Español Spanish](README_es.md)] [[🇨🇦 🇫🇷 Français French](README_fr.md)] [[🇮🇹 Italiano Italian](README_it.md)] [[🇯🇵 日本語 Japanese](README_ja.md)] [[🇧🇷 Português Portuguese](README_pt.md)] [[🇨🇳 中文 Chinese](README.md)]

## Regional List

| Region Code | Time Zone                                        | Remarks                                           |
| :---------: | :----------------------------------------------- | :------------------------------------------------ |
|   `de-DE`   | [`Europe/Berlin`](https://time.is/Germany)       |                                                   |
|   `en-CA`   | [`America/Toronto`](https://time.is/Canada)      |                                                   |
|   `en-GB`   | [`Europe/London`](https://time.is/England)       |                                                   |
|   `en-IN`   | [`Asia/Kolkata`](https://time.is/India)          | `hi-IN` is almost identical and is also discarded |
|   `en-US`   | [`America/Los_Angeles`](https://time.is/Redmond) |                                                   |
|   `es-ES`   | [`Europe/Madrid`](https://time.is/Spain)         |                                                   |
|   `fr-CA`   | [`America/Toronto`](https://time.is/Canada)      |                                                   |
|   `fr-FR`   | [`Europe/Paris`](https://time.is/France)         |                                                   |
|   `it-IT`   | [`Europe/Rome`](https://time.is/Italy)           |                                                   |
|   `ja-JP`   | [`Asia/Tokyo`](https://time.is/Japan)            |                                                   |
|   `pt-BR`   | [`America/Sao_Paulo`](https://time.is/Brazil)    |                                                   |
|   `zh-CN`   | [`Asia/Shanghai`](https://time.is/China)         |                                                   |

See details in [regional_list.csv](regional_list.csv)

## Data Source

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

The returned data structure is represented with [zod](https://zod.dev/) as follows.

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
        ), // It is known that in some regions, data exists that does not match the pattern
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // It is known that in some regions, data exists that does not match the pattern
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // It is known that in some regions, data exists that does not match the pattern
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
      quizId: z.null(), // No values found other than null
      fullDateString: z.string(), // Local date in local language
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // Usually an empty string
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // Usually false
      CTAData: z.null(), // No values found other than null
      detectedRegion: z.string(), // Depends on the region from which the request is sent
      enableBingImageCreator: z.boolean(), // Usually false
      topRightCTAData: z.looseObject({}), // Unimportant data
      imageHotspots: z.null(), // No values found other than null
      AnimatedWP: z.null(), // No values found other than null
    })
  ),
  tooltips: z.looseObject({}), // Unimportant data
  imageCount: z.literal(8),
});
```

## Field List

This project uses jsonl to store data. The data for each locale is placed in the corresponding file under the `data` folder. Each line represents one day's wallpaper, with each day's wallpaper having the following fields:

| Field Name        | Source                                                                              | Remarks                       |
| :---------------- | :---------------------------------------------------------------------------------- | :---------------------------- |
| `date`            | Date obtained by adding the timezone offset (see above) to `images[].fullstartdate` | Date part only                |
| `full_start_time` | `images[].fullstartdate`                                                            | UTC time, precise to the hour |
| `image_url`       | `images[].urlbase`                                                                  | See Note 1                    |
| `copyright`       | `images[].copyrighttext`                                                            |                               |
| `search_url`      | `images[].copyrightlink`                                                            |                               |
| `title`           | `images[].title`                                                                    |                               |
| `description`     | `images[].description`                                                              |                               |
| `headline`        | `images[].headline`                                                                 |                               |
| `quiz_url`        | `images[].quiz`                                                                     |                               |
| `map_image`       | `images[].mapLink.Url`                                                              | See Note 2                    |
| `map_url`         | `images[].mapLink.Link`                                                             | See Note 2                    |

1. `image_url` returns a landscape 4K image (3840x2160) by default. You can crop the image by appending the parameters `&w=<width>&h=<height>&rs=1&c=4`, but be careful not to exceed the image's maximum dimensions.
2. `map_image` and `map_url` are currently only partially available for images in the following regions: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.

## Similar projects

- <https://wallpaper.bokewo.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-CA`、`fr-FR`、`ja-JP`、`zh-CN`)
- <https://dailybing.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://github.com/zkeq/Bing-Wallpaper-Action/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
- <https://bing.gifposter.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://peapix.com/bing/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://bingwallpaper.anerg.com/> (`de-DE`、`en-CA`、`en-GB`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
