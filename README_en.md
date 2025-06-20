# Bing Wallpapers

[[🇩🇪 Deutsch German](README_de.md)] [[🇪🇸 Español Spanish](README_es.md)] [[🇨🇦 🇫🇷 Français French](README_fr.md)] [[🇮🇹 Italiano Italian](README_it.md)] [[🇯🇵 日本語 Japanese](README_ja.md)] [[🇧🇷 Português Portuguese](README_pt.md)] [[🇨🇳 中文 Chinese](README.md)]

## Regional List

| Region Code | Time Zone                                                                                | Remarks                                           |
| :---------: | :--------------------------------------------------------------------------------------- | :------------------------------------------------ |
|   `de-DE`   | Standard Time: `UTC+1`, Daylight Saving Time: `UTC+2`, [Source](https://time.is/Germany) |                                                   |
|   `en-CA`   | Standard Time: `UTC-5`, Daylight Saving Time: `UTC-4`, [Source](https://time.is/Canada)  |                                                   |
|   `en-GB`   | Standard Time: `UTC+0`, Daylight Saving Time: `UTC+1`, [Source](https://time.is/England) |                                                   |
|   `en-IN`   | `UTC+5:30`, [Source](https://time.is/India)                                              | `hi-IN` is almost identical and is also discarded |
|   `en-US`   | Standard Time: `UTC-8`, Daylight Saving Time: `UTC-7`, [Source](https://time.is/Redmond) |                                                   |
|   `es-ES`   | Standard Time: `UTC+1`, Daylight Saving Time: `UTC+2`, [Source](https://time.is/Spain)   |                                                   |
|   `fr-CA`   | Standard Time: `UTC-5`, Daylight Saving Time: `UTC-4`, [Source](https://time.is/Canada)  |                                                   |
|   `fr-FR`   | Standard Time: `UTC+1`, Daylight Saving Time: `UTC+2`, [Source](https://time.is/France)  |                                                   |
|   `it-IT`   | Standard Time: `UTC+1`, Daylight Saving Time: `UTC+2`, [Source](https://time.is/Italy)   |                                                   |
|   `ja-JP`   | `UTC+9`, [Source](https://time.is/Japan)                                                 |                                                   |
|   `pt-BR`   | `UTC-3`, [Source](https://time.is/Brazil)                                                |                                                   |
|   `zh-CN`   | `UTC+8`, [Source](https://time.is/China)                                                 |                                                   |

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
        ), // 	It is known that data exists for the en-GB locale that does not conform to this schema
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // 	It is known that data exists for the en-GB locale that does not conform to this schema
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // 	It is known that data exists for the en-GB locale that does not conform to this schema
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          ),
        Link: z.string().startsWith("https://www.bing.com/maps?"),
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
2. `map_image` and `map_url` are currently only available in the following regions: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.
