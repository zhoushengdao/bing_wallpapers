# Sfondi di Bing

[[🇩🇪 Deutsch Tedesco](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Inglese](README_en.md)] [[🇪🇸 Español Spagnolo](README_es.md)] [[🇨🇦 🇫🇷 Français Francese](README_fr.md)] [[🇯🇵 日本語 Giapponese](README_ja.md)] [[🇧🇷 Português Portoghese](README_pt.md)] [[🇨🇳 中文 Cinese](README.md)]

## Elenco regionale

| Codice Regione | Fuso Orario                                                                | Note                                            |
| :------------: | :------------------------------------------------------------------------- | :---------------------------------------------- |
|    `de-DE`     | Ora Solare: `UTC+1`, Ora Legale: `UTC+2`, [Fonte](https://time.is/Germany) |                                                 |
|    `en-CA`     | Ora Solare: `UTC-5`, Ora Legale: `UTC-4`, [Fonte](https://time.is/Canada)  |                                                 |
|    `en-GB`     | Ora Solare: `UTC+0`, Ora Legale: `UTC+1`, [Fonte](https://time.is/England) |                                                 |
|    `en-IN`     | `UTC+5:30`, [Fonte](https://time.is/India)                                 | `hi-IN` è quasi identico e viene anche scartato |
|    `en-US`     | Ora Solare: `UTC-8`, Ora Legale: `UTC-7`, [Fonte](https://time.is/Redmond) |                                                 |
|    `es-ES`     | Ora Solare: `UTC+1`, Ora Legale: `UTC+2`, [Fonte](https://time.is/Spain)   |                                                 |
|    `fr-CA`     | Ora Solare: `UTC-5`, Ora Legale: `UTC-4`, [Fonte](https://time.is/Canada)  |                                                 |
|    `fr-FR`     | Ora Solare: `UTC+1`, Ora Legale: `UTC+2`, [Fonte](https://time.is/France)  |                                                 |
|    `it-IT`     | Ora Solare: `UTC+1`, Ora Legale: `UTC+2`, [Fonte](https://time.is/Italy)   |                                                 |
|    `ja-JP`     | `UTC+9`, [Fonte](https://time.is/Japan)                                    |                                                 |
|    `pt-BR`     | `UTC-3`, [Fonte](https://time.is/Brazil)                                   |                                                 |
|    `zh-CN`     | `UTC+8`, [Fonte](https://time.is/China)                                    |                                                 |

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
        ), // È noto che esistono dati per la regione en-GB che non si conformano a questo schema
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // È noto che esistono dati per la regione en-GB che non si conformano a questo schema
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // È noto che esistono dati per la regione en-GB che non si conformano a questo schema
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          ),
        Link: z.string().startsWith("https://www.bing.com/maps?"),
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
