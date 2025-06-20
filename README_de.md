# Bing-Hintergrundbilder

[[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Englisch](README_en.md)] [[🇪🇸 Español Spanisch](README_es.md)] [[🇨🇦 🇫🇷 Français Französisch](README_fr.md)] [[🇮🇹 Italiano ](README_it.md)] [[🇯🇵 日本語 Japanisch](README_ja.md)] [[🇧🇷 Português Portugiesisch](README_pt.md)] [[🇨🇳 中文 Chinesisch](README.md)]

## Regionen liste

| Regionencode | Zeitzone                                                                    | Bemerkung                                                 |
| :----------: | :-------------------------------------------------------------------------- | :-------------------------------------------------------- |
|   `de-DE`    | Winterzeit: `UTC+1`, Sommerzeit: `UTC+2`, [Quelle](https://time.is/Germany) |                                                           |
|   `en-CA`    | Winterzeit: `UTC-5`, Sommerzeit: `UTC-4`, [Quelle](https://time.is/Canada)  |                                                           |
|   `en-GB`    | Winterzeit: `UTC+0`, Sommerzeit: `UTC+1`, [Quelle](https://time.is/England) |                                                           |
|   `en-IN`    | `UTC+5:30`, [Quelle](https://time.is/India)                                 | `hi-IN` ist fast identisch und wird ebenfalls weggelassen |
|   `en-US`    | Winterzeit: `UTC-8`, Sommerzeit: `UTC-7`, [Quelle](https://time.is/Redmond) |                                                           |
|   `es-ES`    | Winterzeit: `UTC+1`, Sommerzeit: `UTC+2`, [Quelle](https://time.is/Spain)   |                                                           |
|   `fr-CA`    | Winterzeit: `UTC-5`, Sommerzeit: `UTC-4`, [Quelle](https://time.is/Canada)  |                                                           |
|   `fr-FR`    | Winterzeit: `UTC+1`, Sommerzeit: `UTC+2`, [Quelle](https://time.is/France)  |                                                           |
|   `it-IT`    | Winterzeit: `UTC+1`, Sommerzeit: `UTC+2`, [Quelle](https://time.is/Italy)   |                                                           |
|   `ja-JP`    | `UTC+9`, [Quelle](https://time.is/Japan)                                    |                                                           |
|   `pt-BR`    | `UTC-3`, [Quelle](https://time.is/Brazil)                                   |                                                           |
|   `zh-CN`    | `UTC+8`, [Quelle](https://time.is/China)                                    |                                                           |

Details siehe [regional_list.csv](regional_list.csv)

## Datenquelle

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

Die zurückgegebene Datenstruktur wird mit [zod](https://zod.dev/) wie folgt dargestellt.

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
        ), // Bekannt, dass für die Region en-GB Daten existieren, die nicht diesem Schema entsprechen
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // Bekannt, dass für die Region en-GB Daten existieren, die nicht diesem Schema entsprechen
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // Bekannt, dass für die Region en-GB Daten existieren, die nicht diesem Schema entsprechen
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          ),
        Link: z.string().startsWith("https://www.bing.com/maps?"),
      }),
      quizId: z.null(), // Keine Werte außer null gefunden
      fullDateString: z.string(), // Lokales Datum in der Landessprache
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // Normalerweise leerer String
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // Normalerweise false
      CTAData: z.null(), // Keine Werte außer null gefunden
      detectedRegion: z.string(), // Hängt von der Region ab, von der die Anfrage gesendet wird
      enableBingImageCreator: z.boolean(), // Normalerweise false
      topRightCTAData: z.looseObject({}), // Unwichtige Daten
      imageHotspots: z.null(), // Keine Werte außer null gefunden
      AnimatedWP: z.null(), // Keine Werte außer null gefunden
    })
  ),
  tooltips: z.looseObject({}), // Unwichtige Daten
  imageCount: z.literal(8),
});
```

## Feldliste

| Feldname          | Quelle                                                                                          | Bemerkung                      |
| :---------------- | :---------------------------------------------------------------------------------------------- | :----------------------------- |
| `date`            | Datum, erhalten durch Hinzufügen des Zeitzonen-Offsets (siehe oben) zu `images[].fullstartdate` | Nur Datumsteil                 |
| `full_start_time` | `images[].fullstartdate`                                                                        | UTC-Zeit, genau bis zur Stunde |
| `image_url`       | `images[].urlbase`                                                                              | Siehe Anmerkung 1              |
| `copyright`       | `images[].copyrighttext`                                                                        |                                |
| `search_url`      | `images[].copyrightlink`                                                                        |                                |
| `title`           | `images[].title`                                                                                |                                |
| `description`     | `images[].description`                                                                          |                                |
| `headline`        | `images[].headline`                                                                             |                                |
| `quiz_url`        | `images[].quiz`                                                                                 |                                |
| `map_image`       | `images[].mapLink.Url`                                                                          | Siehe Anmerkung 2              |
| `map_url`         | `images[].mapLink.Link`                                                                         | Siehe Anmerkung 2              |

1. `image_url` liefert standardmäßig ein 4K-Bild (3840x2160) im Querformat. Durch Anhängen der Parameter `&w=<Breite>&h=<Höhe>&rs=1&c=4` kann das Bild zugeschnitten werden, wobei die maximalen Abmessungen des Bildes nicht überschritten werden dürfen.
2. `map_image` und `map_url` werden derzeit nur in den folgenden Regionen bereitgestellt: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.
