# GlacioSeer

**Lead-Time-Conditioned Seasonal Forecasting of Pan-Arctic Sea Ice Concentration With Atmospheric and Oceanic Histories**

> **Code release:** The GlacioSeer source code will be made publicly available at [github.com/yuweikong/GlacioSeer](https://github.com/yuweikong/GlacioSeer) upon acceptance of the manuscript. 

GlacioSeer is a data-driven framework for direct, lead-time-conditioned forecasts of monthly mean pan-Arctic sea-ice concentration (SIC), with forecast leads of one to six months.

An external benchmark against the archived SIPN South submissions of five Antarctic seasons is reported [below](#sipn-south-hindcast-benchmark).

## Model architecture

![Architecture of GlacioSeer-AO](glacioseer_ao_architecture.png)

*Architecture of GlacioSeer-AO. The model combines the SIC forecasting backbone with separately encoded ERA5 atmospheric and ORAS5 oceanic histories.*

GlacioSeer has two configurations:

- **GlacioSeer-SIC** uses the preceding 12 monthly SIC fields. Lead conditioning guides its spatiotemporal processing and temporal readout.
- **GlacioSeer-AO** retains the SIC backbone and adds separate encoders for three-month ERA5 atmospheric and ORAS5 oceanic histories. Variable-axis interaction and latent-slot compression form compact predictor representations; cross-domain interaction and lag-conditioned injection connect them to the SIC pathway. Lead-conditioned readers and feature-wise linear modulation (FiLM) refine the forecast representation before decoding.

The shared network predicts each requested lead directly, without feeding an earlier predicted SIC field into the next forecast step. GlacioSeer-AO uses historical predictor fields and does not require future atmospheric or oceanic forecast fields.

## Reported evaluation

GlacioSeer-AO is evaluated on monthly mean SIC with the spatial anomaly correlation coefficient (SACC), ACC, MAE and IIEE. Under the fixed chronological split (training 1979–2013, validation 2014–2017, evaluation 2018–2025) it outperforms GlacioSeer-SIC at leads 1, 2, 4 and 6 on every metric, and reaches the highest SACC among the compared methods at those leads.

## SIPN South hindcast benchmark

**Both GlacioSeer configurations rank in the top four of every archived SIPN South season, and top the panel in 2024.**

We verify GlacioSeer against every entry archived by [SIPN South](https://sipn-south.org/) for the February forecasts of 2022–2026.

![SIPN South hindcast benchmark](figures/sipn_south/sipn_south_benchmark.png)

*February sea-ice area error against the verifying analysis. Each row is one season; dots are individual submissions, the dashed line is the SIPN climatology and the numbers on the right are the ranks.*

GlacioSeer-SIC ranks second, fourth, first, second and third of 16–22 entries, with errors of 0.015–0.272 × 10⁶ km². In 2024 it is the closest forecast of the whole panel. Its February error is 3 to 33 times smaller than the SIPN climatology in every season, and GlacioSeer-SIC-Rollout follows within 0.047 × 10⁶ km² on average.

<details>
<summary>Full ranking of every submission</summary>

![February SIA error, 2023-2026](figures/sipn_south/feb_sia_ranking_2023_2026.png)

*Every forecast entry of the four most recent seasons, ordered by error. Beyond 1.0 × 10⁶ km² the axis is compressed; the dotted line marks the largest error among the verification products, which sit below the rule as reference analyses.*

</details>

The error table is in [`data/sipn_south_feb_sia_ranking.csv`](data/sipn_south_feb_sia_ranking.csv), and [`scripts/plot_sipn_south_ranking.py`](scripts/plot_sipn_south_ranking.py) reproduces both figures.

## Data sources

The study uses publicly available data; the datasets themselves are not included in this repository.

- Monthly SIC: [NOAA/NSIDC Climate Data Record of Passive Microwave Sea Ice Concentration, Version 6 (G02202)](https://doi.org/10.7265/b18j-z797).
- Atmospheric fields: [ERA5 monthly means from the Copernicus Climate Data Store](https://doi.org/10.24381/cds.f17050d7) and [pressure-level products](https://doi.org/10.24381/cds.6860a573).
- Ocean fields: [ORAS5 monthly ocean reanalysis](https://doi.org/10.24381/cds.67e8eeb7).
- External forecast comparison: selected retrospective Sea Ice Outlook submissions archived by the Sea Ice Prediction Network at [Zenodo](https://doi.org/10.5281/zenodo.10124346).
- Verification analyses: [NSIDC-0051 v2](https://nsidc.org/data/nsidc-0051), [NSIDC-0803](https://nsidc.org/data/nsidc-0803), and [OSI-408](https://osi-saf.eumetsat.int/products/osi-408-b).

See the paper for data processing, input-variable definitions, and evaluation protocols.

## Citation

If you use GlacioSeer, please cite the accompanying paper. The final journal citation and DOI will be added here after publication.

## License

A license will be specified when the source code is released.
