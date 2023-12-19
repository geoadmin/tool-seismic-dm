gith# Seismic data management
This project aims to join the field geometry (SPS structure) and the measured seismic data (segy) together. 
From this new database (SeisDM structure) follows a first quality control, a visualisation of the acquired seismic data and a velocity estimation for each source-receiver pairs. 
## Local installation 
```
git clone https://github.com/geoadmin/tool-seismic-dm.git
```

## Requirements
- numpy 
- matplotlib
- pandas
- pyvista
- rasterio
- (obspy)

```
conda env create -f env.yml
pip install -r requirements.txt
```

## Authors aud acknowledgment 
[Andreas Hoelker](andreas.hoelker@geophytec.com)

[Herfried Madritsch](herfried.madritsch@swisstopo.ch)

[Claire Epiney](claire.epiney@swisstopo.ch)

[Milan Beres](Milan.Beres@swisstopo.ch)





