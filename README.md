# **eyetracking-scegram**

## **Setup project and start pipeline**

1. Install Conda according to https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
2. Create conda environment
```console
conda create --name eyetracking python=3.9
```
3. Activate conda environment
```console
conda activate eyetracking
```
4. Install requirements
```console
pip install -r requirements.txt
```
5. Download scegram database (if not already done) from https://www.scenegrammarlab.com/research/development-of-scene-grammar/scegram-database/

6. Modify config.py and add your system to the list at the top, indication where your data folder is located as well where the scegram database folder lies and how many cores you have on your machine, etc.

7. Start pipeline via doit
```console
doit
```

## **Files**
- `data/` eyetracking data (.tsv-files) of subjects
  - `data/raw/` raw eyetracking data (.tsv-files) of subjects
  - `data/fixed/` fixed and cleaned eyetracking data subject files 
  - `data/processed/` processed eyetracking data subject files 
- `figures/` contains created figures
- `tables/` contains .csv-files of tables