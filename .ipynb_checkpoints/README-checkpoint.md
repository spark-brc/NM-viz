# Visualization National Modelling
## 01_Connectivity Checker

### Installation
1. Anaconda Python:
    - If you don’t already have Anaconda Python installed, please install from this link:https://conda.io/miniconda.html  
    - Select the Python 3.7 version. 
        * Important - on Windows, choose option to install “for this user only” (Note, if you already have Anaconda installed, just skip to the next step which you will still need to run)
    - On Windows open the Anaconda Prompt from Start menu (on a Mac/Linux just open a terminal). And paste in this string and execute (this creates a python environment (nm_viz) that will work with our codes):
    ```bash
    conda create -n nm_viz python=3.7 jupyter notebook
    ```
    - Activate the nm_viz environment
    ```bash
    conda activate nm_viz 
    ```
    - Finally, install holoviz and geoviews with other required libraries
    ```bash
    conda install -c pyviz holoviz geoviews
    ```

Then change directory into the examples or drive and launch it with:  
```bash
jupyter notebook
```


    
    
