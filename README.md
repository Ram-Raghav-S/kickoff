# Kickoff - Premier League Insights

In our experience, many sports statistics do not provide enough valuable information for viewers and team management alike to analyze the various aspects of a team's performance with more depth and variety. Also, existing statistics are often quite technical and are not readily viewable in a proper format for the average person.
 

Kickoff aims to solve both of these problems through a **Python CLI** that helps analysts and fans model past Premier League data and gain statistical insights for both individual teams and the overall league.

## Installation

Installing Kickoff is incredibly simple. First, you'll need Python and a Python version of `3.11` or higher. Then, use `pip` to install Kickoff from PyPI with the below command:

 - `pip install kickoff`

    

## Computational Overview

The entirety of our Premier League data is modelled through a Graph Abstract Data Type. Within this graph, we represent the entire history of the league independent of seasons. Each vertex of the graph represents individual teams in the premier league. Hence, the matches played between two opposing teams are represented as undirected edges connecting the corresponding team objects. With this graph, we are able to compute numerous interesting and insightful statistics that can help teams and fans.

## Commands

All of Kickoff's statistics are accessible through easy to use CLI commands. Each command should be prefixed with the `kickoff` name. All the available commands and the corresponding parameters and descriptions are listed below. They can also be found by running `kickoff --help` or `kickoff <command_name> --help>`.

Note that square brackets indicate required arguments while round brackets indicate optional ones. The `topx` argument can be used to limit or expand the number of results.

-   **aggregate averages** [team], [season]
-   **aggregate winrate** [team], (season)
-   **aggregate homevsaway** [team], (season)
    
-   **records winrates** (season), (topx)
    
-   **records streaks** [season], (topx)
    
-   **records comebacks** (season), (topx)
    
-   **records goals** (season), (topx)
    
-   **records fairplay** (season), (topx)
    
-   **records improvement** [season], (topx)
    
-   **optimal fouls** (team), (topx)
    
-   **optimal yellowcards** (team), (topx)
    
-   **optimal referees** [team], (topx)
    
-   **optimal fairestreferees** (topx)
- **predict** [home], [away], [season]

# Gallery





| | |
|:-------------------------:|:-------------------------:|
|<img width="800" alt="Screen Shot 2023-04-03 at 6 24 32 PM" src="https://user-images.githubusercontent.com/44104695/229640248-c723bf09-4339-4a00-a08b-6d6529edad61.png"> List of Available Teams | <img width="800" alt="Screen Shot 2023-04-03 at 6 25 47 PM" src="https://user-images.githubusercontent.com/44104695/229640400-9e63053e-bc35-43ec-96a5-0ba6189085bb.png"> Statistical Averages for Manchester City in 2012-13|
|<img width="800" alt="Screen Shot 2023-04-03 at 6 26 51 PM" src="https://user-images.githubusercontent.com/44104695/229640530-f896d0cd-037a-4b05-a026-071e0928fdb1.png"> Most Goals Scored in the Last 10 Years|<img width="800" alt="Screen Shot 2023-04-03 at 6 27 42 PM" src="https://user-images.githubusercontent.com/44104695/229640665-5e52163c-1079-420a-a7bf-40edd69d7dc4.png"> Highest Streaks in the 2018-19 Season |



## Dependencies

Kickoff is extremely minimal and only uses three packages: `pandas` for cleaning and loading our datasets, `typer` and `rich` for creating a CLI and pretty printing, and `numpy` for weighted average calculations.

## Datasets

Kickoff uses 10 open-source datasets that contain Premier League data  from the 2009-10 season to the 2018-19 season. These datasets are not our own and but can be accessed on [Kaggle](https://www.kaggle.com/datasets/saife245/english-premier-league).
