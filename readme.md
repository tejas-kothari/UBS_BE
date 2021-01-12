# HKUST-UBS Flask Backend

**Note:** You need to have conda already installed
(Refer to: https://docs.conda.io/projects/conda/en/latest/user-guide/install/)

## How to setup?

1. Create folder `csv` in project folder and place csv files inside it
2. Open terminal
3. `cd` into project folder
4. Run `conda env create -f environment.yml` (This will create the conda environment and install the required libraries)

## How to run?

1. Run `conda activate UBS_BE`
2. Run `python app.py`

## How to kill running Flask app on port?

1. Run `lsof -i:5000` and note the PID
2. Run `kill -9 {PID}`
