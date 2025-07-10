# Fonds d'écran Bing

[![Update Bing Wallpaper](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml/badge.svg?event=schedule)](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml)

[[🇩🇪 Deutsch Allemand](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Anglais](README_en.md)] [[🇪🇸 Español Espagnol](README_es.md)] [[🇮🇹 Italiano Italien](README_it.md)] [[🇯🇵 日本語 Japonais](README_ja.md)] [[🇧🇷 Português Portugais](README_pt.md)] [[🇨🇳 中文 Chinois](README.md)]

## Liste régionale

| Code Région | Fuseau Horaire                                   | Remarque                                                 |
| :---------: | :----------------------------------------------- | :------------------------------------------------------- |
|   `de-DE`   | [`Europe/Berlin`](https://time.is/Germany)       |                                                          |
|   `en-CA`   | [`America/Toronto`](https://time.is/Canada)      |                                                          |
|   `en-GB`   | [`Europe/London`](https://time.is/England)       |                                                          |
|   `en-IN`   | [`Asia/Kolkata`](https://time.is/India)          | `hi-IN` est presque identique et est également abandonné |
|   `en-US`   | [`America/Los_Angeles`](https://time.is/Redmond) |                                                          |
|   `es-ES`   | [`Europe/Madrid`](https://time.is/Spain)         |                                                          |
|   `fr-CA`   | [`America/Toronto`](https://time.is/Canada)      |                                                          |
|   `fr-FR`   | [`Europe/Paris`](https://time.is/France)         |                                                          |
|   `it-IT`   | [`Europe/Rome`](https://time.is/Italy)           |                                                          |
|   `ja-JP`   | [`Asia/Tokyo`](https://time.is/Japan)            |                                                          |
|   `pt-BR`   | [`America/Sao_Paulo`](https://time.is/Brazil)    |                                                          |
|   `zh-CN`   | [`Asia/Shanghai`](https://time.is/China)         |                                                          |

Voir les détails dans [regional_list.csv](regional_list.csv)

## Source de données

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

La structure de données renvoyée est représentée avec [zod](https://zod.dev/) comme suit.

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
        ), // Il est connu que dans certaines régions, il existe des données non conformes au motif
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // Il est connu que dans certaines régions, il existe des données non conformes au motif
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // Il est connu que dans certaines régions, il existe des données non conformes au motif
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
      quizId: z.null(), // Aucune valeur trouvée autre que null
      fullDateString: z.string(), // Date locale dans la langue locale
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // Généralement une chaîne vide
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // Généralement false
      CTAData: z.null(), // Aucune valeur trouvée autre que null
      detectedRegion: z.string(), // Dépend de la région d'où la requête est envoyée
      enableBingImageCreator: z.boolean(), // Généralement false
      topRightCTAData: z.looseObject({}), // Données non importantes
      imageHotspots: z.null(), // Aucune valeur trouvée autre que null
      AnimatedWP: z.null(), // Aucune valeur trouvée autre que null
    })
  ),
  tooltips: z.looseObject({}), // Données non importantes
  imageCount: z.literal(8),
});
```

## Liste des champs

Ce projet utilise jsonl pour stocker les données. Les données de chaque locale sont placées dans le fichier correspondant du dossier `data`. Chaque ligne représente un fond d'écran quotidien, chaque fond d'écran quotidien possédant les champs suivants:

| Nom du champ      | Source                                                                                   | Remarques                         |
| :---------------- | :--------------------------------------------------------------------------------------- | :-------------------------------- |
| `date`            | Date obtenue en ajoutant le décalage horaire (voir ci-dessus) à `images[].fullstartdate` | Partie date uniquement            |
| `full_start_time` | `images[].fullstartdate`                                                                 | Heure UTC, précise à l'heure près |
| `image_url`       | `images[].urlbase`                                                                       | Voir Note 1                       |
| `copyright`       | `images[].copyrighttext`                                                                 |                                   |
| `search_url`      | `images[].copyrightlink`                                                                 |                                   |
| `title`           | `images[].title`                                                                         |                                   |
| `description`     | `images[].description`                                                                   |                                   |
| `headline`        | `images[].headline`                                                                      |                                   |
| `quiz_url`        | `images[].quiz`                                                                          |                                   |
| `map_image`       | `images[].mapLink.Url`                                                                   | Voir Note 2                       |
| `map_url`         | `images[].mapLink.Link`                                                                  | Voir Note 2                       |

1. `image_url` retourne par défaut une image 4K paysage (3840x2160). Vous pouvez recadrer l'image en ajoutant les paramètres `&w=<largeur>&h=<hauteur>&rs=1&c=4`, mais veillez à ne pas dépasser les dimensions maximales de l'image.
2. `map_image` et `map_url` ne sont actuellement disponibles que partiellement pour les images dans les régions suivantes: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.

## Projets similaires

- <https://wallpaper.bokewo.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-CA`、`fr-FR`、`ja-JP`、`zh-CN`)
- <https://dailybing.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://github.com/zkeq/Bing-Wallpaper-Action/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
- <https://bing.gifposter.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://peapix.com/bing/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://bingwallpaper.anerg.com/> (`de-DE`、`en-CA`、`en-GB`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
