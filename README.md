# Projektkonzept: Urbane Hitzeinseln in Münster

## Zielsetzung
Untersuchung und Visualisierung urbaner Hitzeinseln in Münster durch Vergleich von Frühjahrs- und Sommerdaten der letzten fünf Jahre. Der Fokus liegt auf:
- Temperaturverteilung nach Flächennutzung
- Einfluss von Vegetation und Bodenfeuchte
- Darstellung relativer sowie absoluter Unterschiede

---

## Datengrundlage

**Satellitendaten:** Landsat 8 / 9 (TIRS)

**Zeitraum:**
- Frühling: 8 cloudfreie Szenen aus März–Mai (letzte 4 Jahre)
- Sommer: 8 cloudfreie Szenen aus Juni–August (letzte 4 Jahre)

**Benötigte Kanäle:**
- TIRS: Band 10 für Oberflächentemperatur (LST)


**Satellitendaten:** Sentinel-2

**Zeitraum:**
- 1 cloudfreie Szenen aus den letzten Jahren

**Benötigte Kanäle:**
- RGB, NIR, SWIR
---

## Verarbeitungsschritte

### 1. Berechnung der Landoberflächentemperatur (LST)
- Umrechnung von DN-Werten → Radianz → Temperatur mittels Planck-Gleichung
  - Dazu werden zunächst alle Landsat Images unter ".\data\landsat-imagery\raw-data\landsat-`{Jahreszeit}`\" abgelegt
  - Danach wird das Programm `clip_and_convert_to_LST.py` ausgeführt
    - Dadurch wurden die Rohdaten auf die area-of-interest zugeschnitten und die Werte von DN zur Oberflächentemperetur überführt
    - Die Ausgabe wird dabei unter ".\data\landsat-imagery\clipped-lst\landsat-`{Jahreszeit}`\" abgelegt

### 2. Bildung saisonaler Temperatur Mittelwerte
- Um für jede Jahreszeit eine saisonale Mittelwertkarte zu erstellen wird danach das Programm `calc_mean_temp.py` ausgeführt
  - Dadurch werden pro Jahreszeit eine Mittelwertkarte unter ".\data\landsat-imagery\raw-data\landsat-`{Jahreszeit}`\" erstellt


---

## Normalisierung

Ziel: Vergleichbarkeit der Temperaturverteilungen zwischen den Jahreszeiten

**Methode:** Z-Transformation (oder alternativ Min-Max-Normalisierung)

Formel:
$T_{norm} = (T - \mu_{Saison}) / \sigma_{Saison}$


Ergebnis: Darstellung relativer Hitze innerhalb der jeweiligen Szene → Frühling und Sommer werden vergleichbar.

---

## Analyse und Visualisierung

### A. Klassifizierung von Flächentypen

**Zielklassen:**
- Infrastruktur (versiegelt)
- Wald
- Gewässer
- Wiese/Feld

**Methodik:** Schwellenwertbasierte oder überwachte Klassifikation

---

### B. Temperaturvergleich pro Klasse

**Darstellung:**
- Boxplots (Whiskerplots) je Klasse:
  - Relative Temperatur im Frühling
  - Relative Temperatur im Sommer

Ziel: Erkennung der typischen thermischen Eigenschaften jeder Landbedeckung.

---

### C. Korrelationen mit Vegetation und Feuchte

**Berechnung von NDVI und NDMI**
- NDVI = (NIR − Red) / (NIR + Red)
- NDMI = (NIR − SWIR) / (NIR + SWIR)

**Visualisierung:** Scatterplots (inkl. Regressionslinie)

**Beziehungen:**
- NDVI vs. LST (Frühling und Sommer separat)
- NDMI vs. LST

Ziel: Quantitative Analyse der Kühlwirkung von Vegetation und Bodenfeuchte.

---

### D. Differenzbild (Sommer − Frühling)

**Berechnung:**
$\Delta T = T_{Sommer} − T_{Frühling}$


**Ziel:** Darstellung des tatsächlichen Temperaturanstiegs im Stadtgebiet

**Darstellung:** Karte mit abgestufter Farblegende

---

## Zusammenfassende Darstellung (Posteraufbau-Vorschlag)

1. Übersichtskarte Münster mit Klassifikation der Flächentypen
2. Temperaturkarten (Frühling und Sommer, normalisiert)
3. Differenzkarte ΔT
4. Whiskerplots pro Klasse (Frühling/Sommer)
5. Scatterplots zu NDVI/LST und NDMI/LST
6. Fazit und Handlungsempfehlungen (z. B. gezielte Begrünung, Entsiegelung)
