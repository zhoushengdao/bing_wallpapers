# Fondos de pantalla de Bing

[[🇩🇪 Deutsch Alemán](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Inglés](README_en.md)] [[🇨🇦 🇫🇷 Français Francés](README_fr.md)] [[🇮🇹 Italiano Italiano](README_it.md)] [[🇯🇵 日本語 Japonés](README_ja.md)] [[🇧🇷 Português Portugués](README_pt.md)] [[🇨🇳 中文 Chino](README.md)]

## Lista regional

| Código de Región | Zona Horaria                                                                                | Observaciones                                  |
| :--------------: | :------------------------------------------------------------------------------------------ | :--------------------------------------------- |
|     `de-DE`      | Horario de Invierno: `UTC+1`, Horario de Verano: `UTC+2`, [Fuente](https://time.is/Germany) |                                                |
|     `en-CA`      | Horario de Invierno: `UTC-5`, Horario de Verano: `UTC-4`, [Fuente](https://time.is/Canada)  |                                                |
|     `en-GB`      | Horario de Invierno: `UTC+0`, Horario de Verano: `UTC+1`, [Fuente](https://time.is/England) |                                                |
|     `en-IN`      | `UTC+5:30`, [Fuente](https://time.is/India)                                                 | `hi-IN` es casi idéntico y también se descarta |
|     `en-US`      | Horario de Invierno: `UTC-8`, Horario de Verano: `UTC-7`, [Fuente](https://time.is/Redmond) |                                                |
|     `es-ES`      | Horario de Invierno: `UTC+1`, Horario de Verano: `UTC+2`, [Fuente](https://time.is/Spain)   |                                                |
|     `fr-CA`      | Horario de Invierno: `UTC-5`, Horario de Verano: `UTC-4`, [Fuente](https://time.is/Canada)  |                                                |
|     `fr-FR`      | Horario de Invierno: `UTC+1`, Horario de Verano: `UTC+2`, [Fuente](https://time.is/France)  |                                                |
|     `it-IT`      | Horario de Invierno: `UTC+1`, Horario de Verano: `UTC+2`, [Fuente](https://time.is/Italy)   |                                                |
|     `ja-JP`      | `UTC+9`, [Fuente](https://time.is/Japan)                                                    |                                                |
|     `pt-BR`      | `UTC-3`, [Fuente](https://time.is/Brazil)                                                   |                                                |
|     `zh-CN`      | `UTC+8`, [Fuente](https://time.is/China)                                                    |                                                |

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
        ), // Se sabe que existen datos para la región en-GB que no se ajustan a este esquema
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // Se sabe que existen datos para la región en-GB que no se ajustan a este esquema
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // Se sabe que existen datos para la región en-GB que no se ajustan a este esquema
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          ),
        Link: z.string().startsWith("https://www.bing.com/maps?"),
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
2. `map_image` y `map_url` están disponibles actualmente solo en las siguientes regiones: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.
