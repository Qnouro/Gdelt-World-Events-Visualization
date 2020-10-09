# Gdelt-World-Events-Visualization

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Gdelt World Events Visualization</h3>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![World Events Map][Visualization-example]](world_map.png)

The following project aims at visualizing the data uploaded by the Gdelt project. Every 15 minutes, a CSV file is uploaded containing world news events. We create a data pipeline to continuously extract the data, transform it and store it (ETL approach) using python and sql.

The project aims at visualization some world events based on the Gdelt project: https://www.gdeltproject.org/.


The work separates over 2 main axes:

  1- Data Engineering through the creation of a data pipeline: Every 15 minutes, a CSV file is uploaded containing world news events. We create a data pipeline to continuously extract the data, transform it and store it (ETL approach) using python and sql
  
  
  2- Data Visualization of the extracted information: The data is afterwards sent to d3js in order to display a world map with the different events including their information and source.
  
The project *should* be compatible with any OS.

### Built With
The data-pipeline part is made with Python and SQL (sqlite3), while the visualization part relies on Javascript though the use of the d3.js framework.
* [D3.js](https://d3js.org/)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The project realies heavily on python3 which is hence needed.

### Installation

1. Clone the repo
2. Install the requirements
```sh
pip install requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

1- In order to use the script, we first need to start the data-pipeline.
```python
python main.py
```
This will quickly populate the dataset with the last 10 released CSV files shared by the Gdelt project, then will continuously check for updates.

2- Start a server using python
```sh
python -m http.server 8000
```
The launch of the server allows us to see the visualization by going to localhost:8000 (or localhost:PORT). If opened at the root of the project, the visualization will be find at localhost:8000/viz/src/worldMap.html. Adapt the url regarding where you started the server.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Soubat Nour - nour.soubat@gmail.com

Project Link: [https://github.com/Qnouro/Gdelt-World-Events-Visualization](https://github.com/Qnouro/Gdelt-World-Events-Visualization)

## Acknowledgment

Thanks to OthneilDrew for the README template: https://github.com/othneildrew/Best-README-Template/blob/master/README.md.



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/Qnouro/Gdelt-World-Events-Visualization/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/nour-soubat
