# Duckweed Hyperspectral Image Analysis for Biological Change Detection

This repository contains a practical project plan and starter structure for building a hyperspectral image processing and AI pipeline for detecting biological, phenotypic, and genotype-related changes in duckweed.

## Project Goal

The goal is to develop a calibrated hyperspectral imaging pipeline that can detect and explain changes in duckweed caused by genotype, genome editing, treatment, stress, or other biological interventions.

Important note: hyperspectral imaging does **not** detect genome changes directly. It detects downstream phenotypic, biochemical, pigment, water-content, stress, growth, or physiological changes that may be associated with genetic or experimental changes.

## Recommended First Research Question

> Given calibrated hyperspectral images of duckweed over time, can we detect whether a plant, well, or line differs from the wild-type or control group, and identify which wavelengths explain the difference?

## Possible AI Tasks

| Biology Question | AI / Image Analysis Task |
|---|---|
| Wild type vs edited line | Classification |
| Before vs after treatment | Temporal change detection |
| Different gene-edited lines | Multi-class classification |
| Early stress before visible symptoms | Anomaly detection |
| Estimate chlorophyll, biomass, nitrogen, or growth | Regression |
| Find spectral regions affected by treatment or mutation | Explainable spectral analysis |

## Dataset Strategy

Because there may be no ready-made public dataset for duckweed + hyperspectral imaging + genome/change detection, the first major task is to create a controlled dataset.

### Minimum Pilot Dataset

| Component | Suggested Minimum |
|---|---|
| Classes | Control and changed/treatment/edited group |
| Biological replicates | 10 wells per class |
| Time points | 3 to 5 time points |
| Batches | 2 independent imaging/growth batches |
| Total observations | About 100 to 200 independent observations |

### Better Dataset

| Component | Suggested Target |
|---|---|
| Classes | Control + multiple edited/treatment groups |
| Biological replicates | 20 to 30 wells per class |
| Time points | 5 or more time points |
| Batches | 3 or more independent batches |
| Total observations | About 500 to 1,000+ independent observations |

Important: pixels and patches are not independent biological samples. Validation should be split by plate, well, genotype, batch, date, or biological replicate, not randomly by pixel.

## Metadata Template

A strong dataset needs strong metadata. A suggested metadata table is included in [`data/metadata_template.csv`](data/metadata_template.csv).

Key fields:

```text
sample_id, plate_id, well_id, genotype, treatment, time_point,
batch, date, camera, wavelength_range, exposure, light_setting,
media, pH, temperature, operator, ground_truth_label
```

## Imaging Protocol

For every imaging session:

1. Warm up the camera and light source.
2. Capture a dark reference.
3. Capture a white reference.
4. Capture the duckweed plate or tray.
5. Repeat white/dark reference if illumination changes.
6. Keep camera height, exposure, integration time, scan speed, light angle, and background constant.
7. Randomize plate or well positions.
8. Avoid water glare and specular reflection.

For duckweed, water reflection is a major issue. Use controlled lighting, fixed geometry, and a dark non-reflective background where possible.

## Required Hyperspectral Corrections

### 1. Radiometric Correction

Convert raw intensity to reflectance:

```text
Reflectance = (Raw - Dark) / (White - Dark)
```

### 2. Bad Band Removal

Remove bands with:

- Low signal-to-noise ratio
- Saturation
- Sensor edge noise
- Lamp instability
- Strong water absorption regions, especially if using SWIR
- Striping or dead pixels

### 3. Illumination Correction

Correct or control:

- Vignetting
- Uneven illumination
- Shadows
- Specular reflection
- Light source drift

### 4. Segmentation

Separate:

- Duckweed fronds
- Water
- Tray/well material
- Background
- Shadows/glare

The model should learn from plant pixels, not water or tray pixels.

### 5. Spectral Preprocessing

Possible preprocessing methods:

- Savitzky-Golay smoothing
- First derivative spectra
- Standard normal variate normalization
- Multiplicative scatter correction
- Per-band z-score normalization using training data only

Keep both raw calibrated reflectance and processed reflectance.

## Modeling Roadmap

### Stage 1: Classical Baselines

Start with interpretable models before deep learning.

Extract from each plant, well, or ROI:

- Mean spectrum
- Median spectrum
- Spectral standard deviation
- Vegetation indices
- PCA components
- Derivative spectra
- Frond area and growth rate

Train:

- PCA / UMAP for visualization
- Logistic regression
- Random forest
- SVM
- PLS-DA for classification
- PLSR for biochemical or growth regression

### Stage 2: Spectral Deep Learning

After the baseline works, try:

- 1D CNN on spectra
- MLP on selected wavelengths
- Autoencoder for anomaly detection
- Contrastive or self-supervised pretraining on unlabeled duckweed cubes

### Stage 3: Spectral-Spatial Deep Learning

When enough data exists, try:

- 2D CNN on selected band images
- 3D CNN on hyperspectral patches
- Spectral-spatial transformer
- Siamese model for before/after change detection

## Change Detection Strategy

Use each plant or well as its own baseline when possible.

```text
Delta spectrum = Spectrum_day_X - Spectrum_day_0
```

or

```text
Ratio spectrum = Spectrum_day_X / Spectrum_day_0
```

Then compare:

- Edited line vs wild type
- Treatment vs mock treatment
- Later time point vs Day 0
- Different biological batches

This reduces batch effects and helps the model focus on biological change.

## Ground Truth Labels

Useful labels include:

| Label Type | Examples |
|---|---|
| Genetic | wild type, edited line A, edited line B |
| Treatment | control, nutrient stress, chemical stress, induction |
| Time | 0h, 24h, 48h, 72h, 7d |
| Phenotype | frond area, growth rate, chlorophyll, biomass |
| Molecular | qPCR, sequencing confirmation, expression level |
| Expert score | visible phenotype, severity score |

The strongest scientific result will connect hyperspectral features to biological meaning, not only classification accuracy.

## Validation Rules

Avoid random pixel or patch splitting. This causes data leakage.

Recommended validation:

- Train on some batches and test on an unseen batch
- Train on some plates and test on unseen plates
- Train on some biological replicates and test on unseen replicates
- Test on a completely new imaging date

Report:

- Accuracy
- F1-score
- ROC-AUC
- Confusion matrix
- Sensitivity to early change
- Time-to-detection
- Important wavelengths

## Can Similar Public Datasets Be Used?

Yes, but only for limited purposes.

Use public plant hyperspectral datasets to:

- Test preprocessing code
- Build dataloaders
- Test 1D/3D CNN pipelines
- Pretrain feature extractors
- Compare segmentation methods
- Learn band-selection strategies

Do not claim that a model trained on grape, corn, soybean, Arabidopsis, or weed datasets automatically works for duckweed. Species, camera, illumination, water background, and growth system differences matter.

## First 30-Day Plan

### Week 1: Biology + SOP

Write a one-page protocol defining:

- What changed in duckweed
- What classes or labels exist
- What time points are important
- How many replicates are needed
- What ground truth is available
- Exact imaging settings

### Week 2: Pilot Imaging

Capture:

- White and dark references
- 5 to 10 control wells
- 5 to 10 changed wells
- 3 to 5 time points

Build:

- ENVI/NumPy loader
- Calibration pipeline
- Segmentation pipeline
- ROI extraction
- Metadata table

### Week 3: Baseline Analysis

Run:

- PCA
- Mean spectra plots
- Wavelength importance analysis
- SVM / random forest / PLS-DA
- Simple change detection from Day 0

### Week 4: Scale Decision

Answer:

- Are there measurable spectral differences?
- Which time point is most informative?
- Which wavelengths matter?
- How many more samples are needed?
- Is deep learning justified?

## Suggested Repository Structure

```text
duckweed_hsi/
  data/
    raw/
    calibrated/
    masks/
    metadata_template.csv
  docs/
    project_plan.md
  notebooks/
    01_visualize_cube.ipynb
    02_calibration_check.ipynb
    03_baseline_models.ipynb
  src/
    io.py
    calibration.py
    segmentation.py
    features.py
    models.py
    evaluation.py
  configs/
    camera_config_template.yaml
    experiment_config_template.yaml
  results/
    spectra_plots/
    model_reports/
```

## Recommended First Deliverable

> A calibrated hyperspectral imaging pipeline for early detection and explanation of genotype/treatment-induced phenotypic changes in duckweed.

This is realistic, scientifically useful, and publishable if the dataset is designed carefully.

## References and Useful Resources

- Arabidopsis hyperspectral phenotyping study: https://pubmed.ncbi.nlm.nih.gov/22470059/
- Duckweed high-throughput phenotyping study: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0287739
- Duckweed phenotyping Dryad dataset: https://datadryad.org/dataset/doi:10.5061/dryad.t4b8gtj6t
- USDA proximal crop/weed hyperspectral dataset: https://agdatacommons.nal.usda.gov/articles/media/Proximal_Hyperspectral_Image_Dataset_of_Various_Crops_and_Weeds_for_Classification_via_Machine_Learning_and_Deep_Learning_Techniques/25306255
- Grapevine leaf hyperspectral dataset: https://www.nature.com/articles/s41597-023-02642-w
- PlantCV hyperspectral calibration documentation: https://plantcv.readthedocs.io/en/stable/calibrate/
- Plant hyperspectral imaging review: https://link.springer.com/article/10.1186/s13007-017-0233-z
