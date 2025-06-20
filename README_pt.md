# BPapéis de parede do Bing

[[🇩🇪 Deutsch Alemão](README_de.md)] [[🇨🇦 🇬🇧 🇮🇳 🇺🇸 English Inglês](README_en.md)] [[🇪🇸 Español Espanhol](README_es.md)] [[🇨🇦 🇫🇷 Français Francês](README_fr.md)] [[🇮🇹 Italiano Italiano](README_it.md)] [[🇯🇵 日本語 Japonês](README_ja.md)] [[🇨🇳 中文 Chinês](README.md)]

## Lista regional

| Código de Região | Fuso Horário                                                                         | Observações                                    |
| :--------------: | :----------------------------------------------------------------------------------- | :--------------------------------------------- |
|     `de-DE`      | Horário Padrão: `UTC+1`, Horário de Verão: `UTC+2`，[Fonte](https://time.is/Germany) |                                                |
|     `en-CA`      | Horário Padrão: `UTC-5`, Horário de Verão: `UTC-4`，[Fonte](https://time.is/Canada)  |                                                |
|     `en-GB`      | Horário Padrão: `UTC+0`, Horário de Verão: `UTC+1`，[Fonte](https://time.is/England) |                                                |
|     `en-IN`      | `UTC+5:30`，[Fonte](https://time.is/India)                                           | `hi-IN` é quase idêntico e também é descartado |
|     `en-US`      | Horário Padrão: `UTC-8`, Horário de Verão: `UTC-7`，[Fonte](https://time.is/Redmond) |                                                |
|     `es-ES`      | Horário Padrão: `UTC+1`, Horário de Verão: `UTC+2`，[Fonte](https://time.is/Spain)   |                                                |
|     `fr-CA`      | Horário Padrão: `UTC-5`, Horário de Verão: `UTC-4`，[Fonte](https://time.is/Canada)  |                                                |
|     `fr-FR`      | Horário Padrão: `UTC+1`, Horário de Verão: `UTC+2`，[Fonte](https://time.is/France)  |                                                |
|     `it-IT`      | Horário Padrão: `UTC+1`, Horário de Verão: `UTC+2`，[Fonte](https://time.is/Italy)   |                                                |
|     `ja-JP`      | `UTC+9`，[Fonte](https://time.is/Japan)                                              |                                                |
|     `pt-BR`      | `UTC-3`，[Fonte](https://time.is/Brazil)                                             |                                                |
|     `zh-CN`      | `UTC+8`，[Fonte](https://time.is/China)                                              |                                                |

Ver detalhes em [regional_list.csv](regional_list.csv)

## Fonte de dados

[https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=](https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt=)

A estrutura de dados retornada é representada com [zod](https://zod.dev/) da seguinte forma.

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
        ), // Sabe-se que existem dados na região en-GB que não estão em conformidade com este padrão
      copyrighttext: z.string().startsWith("© "),
      copyrightlink: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=([^&]+)&form=BGALM(?:&filters=HpDate:"(\d{8}_\d{4})")$/
        ), // Sabe-se que existem dados na região en-GB que não estão em conformidade com este padrão
      title: z.string(),
      description: z.string(),
      headline: z.string(),
      quiz: z
        .string()
        .regex(
          /^https:\/\/www\.bing\.com\/search\?q=Bing\+homepage\+quiz&filters=WQOskey:"HPQuiz_(\d{8})_([^"]+)"&FORM=BGAQ$/
        ), // Sabe-se que existem dados na região en-GB que não estão em conformidade com este padrão
      mapLink: z.object({
        Url: z
          .string()
          .startsWith(
            "https://platform.bing.com/geo/REST/v1/Imagery/Map/RoadVibrant/"
          ),
        Link: z.string().startsWith("https://www.bing.com/maps?"),
      }),
      quizId: z.null(), // Nenhum valor encontrado além de null
      fullDateString: z.string(), // Data local no idioma local
      theme: z.tuple([z.literal("bing")]),
      travelUrl: z.string().startsWith("https://www.bing.com/"),
      visualSearchUrl: z.string(), // Geralmente uma string vazia
      sourceType: z.literal("BingImageOfTheDay"),
      showVisualSearch: z.boolean(), // Geralmente false
      CTAData: z.null(), // Nenhum valor encontrado além de null
      detectedRegion: z.string(), // Depende da região de onde a solicitação é enviada
      enableBingImageCreator: z.boolean(), // Geralmente false
      topRightCTAData: z.looseObject({}), // Dados não importantes
      imageHotspots: z.null(), // Nenhum valor encontrado além de null
      AnimatedWP: z.null(), // Nenhum valor encontrado além de null
    })
  ),
  tooltips: z.looseObject({}), // Dados não importantes
  imageCount: z.literal(8),
});
```

## Lista de campos

| Nome do campo     | Origem                                                                                    | Observações                     |
| :---------------- | :---------------------------------------------------------------------------------------- | :------------------------------ |
| `date`            | Data obtida ao adicionar o offset de fuso horário (ver acima) ao `images[].fullstartdate` | Apenas a parte da data          |
| `full_start_time` | `images[].fullstartdate`                                                                  | Horário UTC, preciso até a hora |
| `image_url`       | `images[].urlbase`                                                                        | Ver Nota 1                      |
| `copyright`       | `images[].copyrighttext`                                                                  |                                 |
| `search_url`      | `images[].copyrightlink`                                                                  |                                 |
| `title`           | `images[].title`                                                                          |                                 |
| `description`     | `images[].description`                                                                    |                                 |
| `headline`        | `images[].headline`                                                                       |                                 |
| `quiz_url`        | `images[].quiz`                                                                           |                                 |
| `map_image`       | `images[].mapLink.Url`                                                                    | Ver Nota 2                      |
| `map_url`         | `images[].mapLink.Link`                                                                   | Ver Nota 2                      |

1. `image_url` retorna por padrão uma imagem 4K paisagem (3840x2160). É possível redimensionar adicionando `&w=<largura>&h=<altura>&rs=1&c=4`, mas sem exceder as dimensões máximas.
2. `map_image` e `map_url` estão disponíveis apenas nestas regiões: `de-DE`, `en-CA`, `en-GB`, `en-IN`, `en-US`, `fr-CA`, `fr-FR`, `it-IT`, `ja-JP`.
