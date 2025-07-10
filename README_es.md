# Fondos de pantalla de Bing

[![Update Bing Wallpaper](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml/badge.svg?event=schedule)](https://github.com/zhoushengdao/bing_wallpapers/actions/workflows/update.yaml)

[[🇩🇪 Deutsch Alemán](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Inglés](README_en.md)] [[🇨🇦 🇫🇷 Français Francés](README_fr.md)] [[🇮🇹 Italiano Italiano](README_it.md)] [[🇯🇵 日本語 Japonés](README_ja.md)] [[🇧🇷 Português Portugués](README_pt.md)] [[🇨🇳 中文 Chino](README.md)]

## Lista regional

| Código de Región | Zona Horaria                                     | Observaciones                                  |
| :--------------: | :----------------------------------------------- | :--------------------------------------------- |
|     `de-DE`      | [`Europe/Berlin`](https://time.is/Germany)       |                                                |
|     `en-CA`      | [`America/Toronto`](https://time.is/Canada)      |                                                |
|     `en-GB`      | [`Europe/London`](https://time.is/England)       |                                                |
|     `en-IN`      | [`Asia/Kolkata`](https://time.is/India)          | `hi-IN` es casi idéntico y también se descarta |
|     `en-US`      | [`America/Los_Angeles`](https://time.is/Redmond) |                                                |
|     `es-ES`      | [`Europe/Madrid`](https://time.is/Spain)         |                                                |
|     `fr-CA`      | [`America/Toronto`](https://time.is/Canada)      |                                                |
|     `fr-FR`      | [`Europe/Paris`](https://time.is/France)         |                                                |
|     `it-IT`      | [`Europe/Rome`](https://time.is/Italy)           |                                                |
|     `ja-JP`      | [`Asia/Tokyo`](https://time.is/Japan)            |                                                |
|     `pt-BR`      | [`America/Sao_Paulo`](https://time.is/Brazil)    |                                                |
|     `zh-CN`      | [`Asia/Shanghai`](https://time.is/China)         |                                                |

Ver detalles en [regional_list.csv](regional_list.csv)

## Fuente de datos

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

La estructura de datos devuelta se representa con [zod](https://zod.dev/) de la siguiente manera.

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
        ), // Se sabe que en algunas regiones existen datos que no coinciden con el patrón
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // Se sabe que en algunas regiones existen datos que no coinciden con el patrón
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // Se sabe que en algunas regiones existen datos que no coinciden con el patrón
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
      quizId: z.null(), // No se encontraron valores distintos de null
      fullDateString: z.string(), // Fecha local en idioma local
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // Generalmente una cadena vacía
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // Generalmente false
      CTAData: z.null(), // No se encontraron valores distintos de null
      detectedRegion: z.string(), // Depende de la región desde la que se envía la solicitud
      enableBingImageCreator: z.boolean(), // Generalmente false
      topRightCTAData: z.looseObject({}), // Datos no importantes
      imageHotspots: z.null(), // No se encontraron valores distintos de null
      AnimatedWP: z.null(), // No se encontraron valores distintos de null
    })
  ),
  tooltips: z.looseObject({}), // Datos no importantes
  imageCount: z.literal(8),
});
```

## Lista de campos

Este proyecto utiliza jsonl para almacenar datos. Los datos de cada localidad se almacenan en el archivo correspondiente dentro de la carpeta `data`. Cada línea representa el fondo de pantalla de un día, y cada fondo de pantalla diario contiene los siguientes campos:

| Nombre del campo  | Origen                                                                                             | Observaciones                   |
| :---------------- | :------------------------------------------------------------------------------------------------- | :------------------------------ |
| `date`            | Fecha obtenida al añadir el desplazamiento de zona horaria (ver arriba) a `images[].fullstartdate` | Solo parte de la fecha          |
| `full_start_time` | `images[].fullstartdate`                                                                           | Hora UTC, precisa hasta la hora |
| `image_url`       | `images[].urlbase`                                                                                 | Ver Nota 1                      |
| `copyright`       | `images[].copyrighttext`                                                                           |                                 |
| `search_url`      | `images[].copyrightlink`                                                                           |                                 |
| `title`           | `images[].title`                                                                                   |                                 |
| `description`     | `images[].description`                                                                             |                                 |
| `headline`        | `images[].headline`                                                                                |                                 |
| `quiz_url`        | `images[].quiz`                                                                                    |                                 |
| `map_image`       | `images[].mapLink.Url`                                                                             | Ver Nota 2                      |
| `map_url`         | `images[].mapLink.Link`                                                                            | Ver Nota 2                      |

1. `image_url` devuelve una imagen 4K apaisada (3840x2160) por defecto. Puedes recortar la imagen añadiendo los parámetros `&w=<ancho>&h=<alto>&rs=1&c=4`, pero ten cuidado de no exceder las dimensiones máximas de la imagen.
2. `map_image` y `map_url` actualmente solo están disponibles parcialmente para imágenes en las siguientes regiones: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.

## Proyectos similares

- <https://wallpaper.bokewo.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-CA`、`fr-FR`、`ja-JP`、`zh-CN`)
- <https://dailybing.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://github.com/zkeq/Bing-Wallpaper-Action/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
- <https://bing.gifposter.com/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://peapix.com/bing/> (`de-DE`、`en-CA`、`en-GB`、`en-IN`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`pt-BR`、`zh-CN`)
- <https://bingwallpaper.anerg.com/> (`de-DE`、`en-CA`、`en-GB`、`en-US`、`es-ES`、`fr-FR`、`it-IT`、`ja-JP`、`zh-CN`)
