# GlacioSeer

**Lead-Time-Conditioned Seasonal Forecasting of Pan-Arctic Sea Ice Concentration With Atmospheric and Oceanic Histories**

> **Code release:** The GlacioSeer source code will be made publicly available at [github.com/yuweikong/GlacioSeer](https://github.com/yuweikong/GlacioSeer) upon acceptance of the manuscript. This page describes the model and its reported evaluation; executable code and run instructions will be added with the release.

GlacioSeer is a data-driven framework for direct, lead-time-conditioned forecasts of monthly mean pan-Arctic sea-ice concentration (SIC), with forecast leads of one to six months.

## Model architecture

![Architecture of GlacioSeer-AO](figures/glacioseer_ao_architecture.png)

*Architecture of GlacioSeer-AO. The model combines the SIC forecasting backbone with separately encoded ERA5 atmospheric and ORAS5 oceanic histories. The diagram is also available as a [PDF figure](figures/glacioseer_ao_architecture.pdf).*

GlacioSeer has two configurations:

- **GlacioSeer-SIC** uses the preceding 12 monthly SIC fields. Lead conditioning guides its spatiotemporal processing and temporal readout.
- **GlacioSeer-AO** retains the SIC backbone and adds separate encoders for three-month ERA5 atmospheric and ORAS5 oceanic histories. Variable-axis interaction and latent-slot compression form compact predictor representations; cross-domain interaction and lag-conditioned injection connect them to the SIC pathway. Lead-conditioned readers and feature-wise linear modulation (FiLM) refine the forecast representation before decoding.

The shared network predicts each requested lead directly, without feeding an earlier predicted SIC field into the next forecast step. GlacioSeer-AO uses historical predictor fields and does not require future atmospheric or oceanic forecast fields.

## Reported evaluation

The manuscript evaluates monthly mean SIC with the spatial anomaly correlation coefficient (SACC), anomaly correlation coefficient (ACC), mean absolute error (MAE), and integrated ice-edge error (IIEE).

Under the fixed chronological split (training: 1979–2013; validation: 2014–2017; evaluation: 2018–2025), GlacioSeer-AO has higher SACC and ACC and lower MAE and IIEE than GlacioSeer-SIC at forecast leads 1, 2, 4, and 6. Among the methods compared under this split, it achieves the highest SACC at those four leads and ranks in the top two for every reported metric–lead pair. Rolling-origin results vary by lead and target season.

These are retrospective hindcasts using finalized SIC and reanalysis fields. The study does not evaluate whether those finalized inputs would have been available in real time at each nominal initialization date.

## Data sources

The study uses publicly available data; the datasets themselves are not included in this repository.

- Monthly SIC: [NOAA/NSIDC Climate Data Record of Passive Microwave Sea Ice Concentration, Version 6 (G02202)](https://doi.org/10.7265/b18j-z797).
- Atmospheric fields: [ERA5 monthly means from the Copernicus Climate Data Store](https://doi.org/10.24381/cds.f17050d7) and [pressure-level products](https://doi.org/10.24381/cds.6860a573).
- Ocean fields: [ORAS5 monthly ocean reanalysis](https://doi.org/10.24381/cds.67e8eeb7).
- External forecast comparison: selected retrospective Sea Ice Outlook submissions archived by the Sea Ice Prediction Network at [Zenodo](https://doi.org/10.5281/zenodo.10124346).

See the paper for data processing, input-variable definitions, and evaluation protocols.

## Citation

If you use GlacioSeer, please cite the accompanying paper. The final journal citation and DOI will be added here after publication.

## License

A license will be specified when the source code is released.
