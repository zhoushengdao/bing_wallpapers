# Sfondi di Bing

[![Update Bing Wallpaper](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml/badge.svg?event=schedule)](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml)

[[🇩🇪 Deutsch Tedesco](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Inglese](README_en.md)] [[🇪🇸 Español Spagnolo](README_es.md)] [[🇨🇦 🇫🇷 Français Francese](README_fr.md)] [[🇯🇵 日本語 Giapponese](README_ja.md)] [[🇧🇷 Português Portoghese](README_pt.md)] [[🇨🇳 中文 Cinese](README.md)]

## Elenco regionale

| Codice Regione | Fuso Orario                                      | Note                                            |
| :------------: | :----------------------------------------------- | :---------------------------------------------- |
|    `de-DE`     | [`Europe/Berlin`](https://time.is/Germany)       |                                                 |
|    `en-CA`     | [`America/Toronto`](https://time.is/Canada)      |                                                 |
|    `en-GB`     | [`Europe/London`](https://time.is/England)       |                                                 |
|    `en-IN`     | [`Asia/Kolkata`](https://time.is/India)          | `hi-IN` è quasi identico e viene anche scartato |
|    `en-US`     | [`America/Los_Angeles`](https://time.is/Redmond) |                                                 |
|    `es-ES`     | [`Europe/Madrid`](https://time.is/Spain)         |                                                 |
|    `fr-CA`     | [`America/Toronto`](https://time.is/Canada)      |                                                 |
|    `fr-FR`     | [`Europe/Paris`](https://time.is/France)         |                                                 |
|    `it-IT`     | [`Europe/Rome`](https://time.is/Italy)           |                                                 |
|    `ja-JP`     | [`Asia/Tokyo`](https://time.is/Japan)            |                                                 |
|    `pt-BR`     | [`America/Sao_Paulo`](https://time.is/Brazil)    |                                                 |
|    `zh-CN`     | [`Asia/Shanghai`](https://time.is/China)         |                                                 |

Vedi dettagli in [regional_list.csv](regional_list.csv)

## Fonte dei dati

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

La struttura dei dati restituita è rappresentata con [zod](https://zod.dev/) come segue.

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
        ), // È noto che in alcune regioni esistono dati non conformi al pattern
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // È noto che in alcune regioni esistono dati non conformi al pattern
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // È noto che in alcune regioni esistono dati non conformi al pattern
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
      quizId: z.null(), // Nessun valore trovato diverso da null
      fullDateString: z.string(), // Data locale nella lingua locale
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // Generalmente una stringa vuota
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // Generalmente false
      CTAData: z.null(), // Nessun valore trovato diverso da null
      detectedRegion: z.string(), // Dipende dalla regione da cui viene inviata la richiesta
      enableBingImageCreator: z.boolean(), // Generalmente false
      topRightCTAData: z.looseObject({}), // Dati non importanti
      imageHotspots: z.null(), // Nessun valore trovato diverso da null
      AnimatedWP: z.null(), // Nessun valore trovato diverso da null
    })
  ),
  tooltips: z.looseObject({}), // Dati non importanti
  imageCount: z.literal(8),
});
```

## Elenco dei campi

Questo progetto utilizza jsonl per memorizzare i dati. I dati di ogni locale sono collocati nel file corrispondente nella cartella `data`. Ogni riga rappresenta lo sfondo del giorno, e ogni sfondo giornaliero possiede i seguenti campi:

| Nome del campo    | Origine                                                                                    | Note                     |
| :---------------- | :----------------------------------------------------------------------------------------- | :----------------------- |
| `date`            | Data ottenuta aggiungendo l'offset del fuso orario (vedi sopra) a `images[].fullstartdate` | Solo la parte della data |
| `full_start_time` | `images[].fullstartdate`                                                                   | Ora UTC, precisa all'ora |
| `image_url`       | `images[].urlbase`                                                                         | Vedi Nota 1              |
| `copyright`       | `images[].copyrighttext`                                                                   |                          |
| `search_url`      | `images[].copyrightlink`                                                                   |                          |
| `title`           | `images[].title`                                                                           |                          |
| `description`     | `images[].description`                                                                     |                          |
| `headline`        | `images[].headline`                                                                        |                          |
| `quiz_url`        | `images[].quiz`                                                                            |                          |
| `map_image`       | `images[].mapLink.Url`                                                                     | Vedi Nota 2              |
| `map_url`         | `images[].mapLink.Link`                                                                    | Vedi Nota 2              |

1. `image_url` restituisce per impostazione predefinita un'immagine 4K orizzontale (3840x2160). È possibile ritagliare l'immagine aggiungendo i parametri `&w=<larghezza>&h=<altezza>&rs=1&c=4`, ma fare attenzione a non superare le dimensioni massime dell'immagine.
2. `map_image` e `map_url` sono attualmente disponibili solo parzialmente per le immagini nelle seguenti regioni: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.

## Progetti simili

- <https://wallpaper.bokewo.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-CA`、`fr-FR`、`ja-JP`、`zh-CN`)
- <https://dailybing.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://github.com/zkeq/Bing-Wallpaper-Action/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
- <https://bing.gifposter.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://peapix.com/bing/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://bingwallpaper.anerg.com/> (`de-DE`、`en-CA`、`en-GB`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
