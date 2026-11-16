# Sales Report Dashboard (Power BI → Web)

**Live demo:** https://diimasogan.github.io/PowerBI-SalesReport-Dashboard/

An interactive property sales report, originally built in Power BI and rebuilt as a static web page so it can be explored without a Power BI licence.

## Features
- **Global filters:** Province, City, SBU, Division, Cluster, Product type and SO year range. Clicking a bar or map bubble also filters the report.
- **Overview:** KPI tiles, a bubble map of net sales by city, net sales by province, the top 10 cities, net sales by SBU and by product type, and monthly cancellation trends.
- **Summary:** a province → city table that expands when you click a province.
- **Detail:** a sortable, searchable and paginated table.
- Light and dark mode, plus a responsive layout for mobile.

## Data
⚠️ **All data is anonymized.** Company, division and cluster names are replaced with generic labels, SBU names are generalised, and every amount is scaled by a hidden factor with random noise added per row. The trends look realistic, but the figures are not real.

`data.json` is a pre-aggregated version of the anonymized dataset (about 57k grouped rows from 87k sales-order lines).

## Tech
Plain HTML, CSS and JavaScript, [Apache ECharts](https://echarts.apache.org/) for the charts, and [Leaflet](https://leafletjs.com/) with OpenStreetMap tiles for the map. There is no build step, and it is hosted on GitHub Pages.

## Power BI → web mapping
| Power BI | Web |
|---|---|
| Slicers (Province, City, SBU, Division, Cluster, Product Type, SO Date) | Filter bar |
| Azure Map (Province / City) | Leaflet bubble map |
| Top 10 bar charts, donut chart | ECharts horizontal bars |
| Cancellation line chart (`Cancellation Province` measure) | ECharts line chart (count of `ZC*` order types) |
| Matrix (Summary page) | Expandable province → city table |
| Table + drill-through (Detail pages) | Sortable, searchable detail table |
