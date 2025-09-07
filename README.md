# COVID Simulation
Disease model to assist with the following research project.

_What was the role of epidemic modelling in influencing government policies against COVID-19?  
A comparison of the policies used by England and Sweden in March to December 2020._

## Navigating the repository

### Data Analysis
The data analysis is contained in the `data_analysis` folder, which contains python scripts for data cleaning and analysis.  
The result from the data analysis is used directly in the `project` file.  

### Docs
Documentation for the project, split up into the different sections.  
The `log.md` file contains a log of the project, including the research and development process, and any changes I made to the project.  

### Project
The project file, which contains the project itself.

## To run
### Normally
```bash
./render.sh [Scene Name]
```

### With Docker
Must be in the project directory.
#### Windows cmd - Does NOT work with Git Bash or if the path contains spaces
```
docker run --rm -it -v %cd%:/manim manimcommunity/manim manim main.py Simulation
```
#### Windows Powershell
```powershell
docker run --rm -it -v ${pwd}:/manim manimcommunity/manim manim main.py Simulation
```

#### Linux
```bash
docker run --rm -it -v $(pwd):/manim manimcommunity/manim manim main.py Simulation
```

### Time to render
On my machine (i5-12400) the rendering time is around 2.5 seconds for each second of simulation time.
