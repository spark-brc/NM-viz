# National Modelling Visualization

## Get data and jupyter notebooks
You essentially have 2 options:

#### - Easy way
- [Download the data zip file](https://github.com/spark-brc/NM-viz/archive/master.zip)
- Unzip it to a prefered location.

#### - Hard way (Dev mode)  
- You will need to install Git if you don’t have it installed already. Downloads are available at [the link](https://git-scm.com/download). On windows, be sure to select the option that installs command-line tools  
- For Git, you will need to set up SSH keys to work with Github. To do so:
    - Go to GitHub.com and set up an account
    - On Windows, open Git Bash (on Mac/Linux, just open a terminal) and set up ssh keys if you haven’t already. To do this, simply type ssh-keygen in git bash/terminal and accept all defaults (important note - when prompted for an optional passphrase, just hit return.)  
- Follow the [instructions](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) to set up the SSH keys with your GitHub account.
- Clone the materials from GitHub.
    - Open a git bash shell from the start menu (or, on a Mac/Linux, open a terminal)
    - Navigate to the folder you made to put the course materials
    - Clone the materials by executing the following in the git bash or terminal window:    

    ```bash
    git clone https://github.com/spark-brc/NM-viz.git
    ```  
        
## Installation
To execute jupyter notebook, we need the Anaconda environment.

#### 1. Anaconda Python:
- If you don’t already have Anaconda Python installed, please install from this link:https://conda.io/miniconda.html  
- Select the Python 3.7 version. 
    * Important - on Windows, choose option to install “for this user only” (Note, if you already have Anaconda installed, just skip to the next step which you will still need to run)

#### 2. Set Environment and install libraries:
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
conda install -c pyviz holoviz geoviews openpyxl
```

Then change directory into the example folder or drive:  
- Change directory (example)
 ```bash
cd NM_viz_master 
```  
- Launch jupyter notebook 
```bash
jupyter notebook
```

A browser window with a Jupyter notebook instance should open.

