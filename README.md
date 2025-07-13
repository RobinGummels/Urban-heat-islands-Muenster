# Saisonale Hitzeinseln im Münsterland

Dieses Repository enthält den vollständigen Workflow sowie alle relevanten Daten und Skripte zur Analyse saisonaler Hitzeinseln im Münsterland. Ziel ist die quantitative Beschreibung der saisonalen Dynamik zwischen Frühling und Sommer, die räumliche Analyse der Landoberflächentemperaturen (LST) in Bezug auf verschiedene Landnutzungstypen und die Bewertung des Einflusses vegetativer und feuchtebezogener Indizes (NDVI, NDMI) auf die Temperaturmuster.

## Übersicht

Die urbane Hitzeinselwirkung ist längst nicht mehr nur ein metropolitanes Phänomen. Versiegelte Flächen speichern tagsüber Wärme und geben diese nachts nur langsam ab, während Vegetationsflächen durch Evapotranspiration eine natürliche Kühlfunktion übernehmen. Diese Studie analysiert die saisonalen Unterschiede in der Hitzeinselbildung im Raum Münster mithilfe satellitengestützter Daten.

## Daten und Methoden

### Rohdaten

Grundlage der Analyse sind Landsat 8/9 Satellitendaten (Rohdaten konnte aufgrund der Größe nicht ins Repository gepusht werden), aufgenommen zwischen 2022 und 2025, welche saisonal (Frühling: März-Mai; Sommer: Juni-August) zusammengefasst wurden. Die atmosphärenkorrigierten Level-2 Daten stammen aus dem USGS Land Surface Analysis Archive (Collection 2, Level-2 SP).

Die LST-Werte wurden aus Band 10 abgeleitet:

```
LST(°C) = DN × M + A − 273,15
```

### Vorverarbeitung

Zur Vergleichbarkeit der saisonalen Temperaturunterschiede wurden die Raster einer z-Normalisierung unterzogen:

```
z = (x - μ) / σ
```

Dabei repräsentiert x die Pixeltemperatur, μ den saisonalen Mittelwert und σ die Standardabweichung.

Die resultierende Δz-Karte (Differenz Sommer-Frühling) zeigt die Veränderung der Hitzeinselwirkung zwischen den Jahreszeiten.

### Landnutzung und Indizes

Die Klassifikation der Landnutzung erfolgte auf Basis einer Sentinel-2-Szene mithilfe eines Random-Forest-Algorithmus in die Klassen Infrastruktur, Wasser, Wald sowie Feld/Wiese.

Zusätzlich wurden der NDVI und NDMI berechnet, um den Einfluss von Vegetation und Bodenfeuchte auf die Temperatur zu analysieren.

## Ergebnisse

Wenn du an dem Gesamtergebnis und an der Interpretation der Ergebnisse unserer Arbeit interessiert bist schaue dir gerne unser Poster `Saisonale_Hitzeinseln_im_Münsterland.pdf` an. Dieses Repository und das Poster wurde im Zusammenhang mit der Prüfungsleistung des Moduls "Einführung in die Fernerkundung" im Sommersemester 2025 an der Universität Münster erstellt.

## Workflow

Um die Analyse vollständig durchzuführen, gehe wie folgt vor:

1. Speichere Landsat-Rohdaten im Ordner `data/landsat-imagery/raw-data` in passenden Unterordnern (z.B. nach Jahreszeiten).
2. Erstelle und speichere die Projekt-Area-of-Interest als Shapefile in `data/project-area`.
3. Speichere deine Landnutzungsklassifikation in `data/sentinel-2/classification`.
4. Berechne und speichere NDVI- und NDMI-Raster in `data/sentinel-2/ndvi-ndmi`.

Starte anschließend das Hauptskript:

```bash
python scripts/run_full_analysis.py
```

Dieses Skript führt automatisch alle einzelnen Prozessschritte (Vorverarbeitung, LST-Berechnung, Normalisierung, Differenz-Berechnung, Korrelation und klassenspezifische-Analyse) aus.

### Repository-Struktur

```
├── data
│   ├── landsat-imagery
│   │   └── raw-data (Hier Landsat-Szenen in Unterordnern nach Jahreszeiten o. Ä. speichern)
│   ├── project-area (Hier Shapefile der Area-of-Interest ergänzen)
│   ├── sentinel-2
│       ├── classification (Landnutzungsklassifikation)
│       └── ndvi-ndmi (Raster der NDVI- und NDMI-Indizes)
├── scripts
│   ├── boxplot_by_class.py
│   ├── clip_and_convert_to_LST.py
│   ├── compute_seasonal_means.py
│   ├── compute_lst_with_indices.py
│   └── deltaZ-statistics.py
│   └── normalize_seasonal_means_z-trans.py
│   └── z_transformed_boxplot_by_class-trans.py
```

## Nutzung und Erweiterung

Der Workflow ist offen gestaltet, sodass mit geringfügigen Anpassungen andere Zeiträume oder Untersuchungsgebiete analysiert werden können. Alle notwendigen Anpassungen erfolgen durch Aktualisierung der Datensätze in den genannten Ordnern. Der klare Aufbau der Python-Skripte unterstützt hierbei eine einfache Anpassung und Erweiterung der Analysen.

## Referenz

Gummels, R., & Kruck, L. (2025). Urban-heat-islands-Muenster \[Source code]. GitHub. [https://github.com/RobinGummels/Urban-heat-islands-Muenster](https://github.com/RobinGummels/Urban-heat-islands-Muenster)

Für Rückfragen stehen wir gerne zur Verfügung. Viel Erfolg bei deiner Analyse!
