# `Project #2 Happiness Atlas: Finding Nirvana`

The goal of this project was to use the Global Happiness Report to model happiness, as measured by the Life Ladder global survey metric, using machine learning models.

## Table of Contents

* [General Information](#general-information)
* [Findings](#findings)
* [The Datasets](#the-datasets)
* [Software and Technologies Used](#software-and-technologies-used)
* [Code and Presentation Files](#code-and-presentation-files)
* [Team Information](#team-information)

## General Information

Gallup has produced an annual Global Happiness Report since 2005 that compiles surveyed measures of happiness, including the Cantril Life Ladder Index, Positive Affect, and Negative Affect, along with academically-sourced indicators of happiness, such as GDP, life expectancy at birth, perceptions of corruption, confidence in government, social support, generosity, and freedom.  We explore the power of machine learning models to predict the Cantril Life Ladder Index using these feature indicators of happiness.  We examine two supervised machine learning algorithms to create two models:
1. Suport Vector Machine (SVM) Regression
2. Neural Net

## Findings

We found that the SVM explained 92% of the training variation and remained robust in testing, explaining 89% of the variation in the Life Ladder Index test dataset.  We confirmed similar levels of mean squared error (MSE) between both our SVM and Neural Net models, both in training and subsequent evaluation of test date.

We presented our findings on October 5, 2023 to the `Columbia Engineering FinTech Bootcamp 2023-06` cohort remotely via Zoom.

Location: [Presentation in GitHub Repository](https://github.com/boz-tcm/happiness_atlas/blob/master/Project%202_%20The%20Neural%20Nets%20.pdf) 

![A screenshot depicts Presentation Cover Page.](Project_2_The_Neural_Nets.jpg)

## The Datasets

We used two datasets, a primary dataset consisting of the happiness measures and features by country (166), and a secondary dataset to augment the primary dataset with regional identification (15 sub-regions).

1. `World Happiness Report 2005-2021 (1).csv`

    (Source: [Kaggle.com](https://www.kaggle.com/datasets/jahaidulislam/world-happiness-report-2005-2021/))
2. `continents2.csv`

    (Source: [Kaggle.com](https://www.kaggle.com/datasets/andradaolteanu/country-mapping-iso-continent-region))

Location: [GitHub Repository](`https://github.com/boz-tcm/happiness_atlas/`)

## Software and Technologies Used

### Development Environment

* Python Version 3.10.12
* git version 2.34.1
* Google Colab Jupyter Notebook 6.5.5

### Libaries

* [Pandas](https://pandas.pydata.org/docs/)
* [Pathlib](https://docs.python.org/3/library/pathlib.html)
* [Numpy](https://numpy.org/doc/stable/)
* [Matplotlib](https://matplotlib.org)
* [hvPlot with Pandas](https://hvplot.holoviz.org)
* [HoloViews](https://holoviews.org)
* [TensorFlow](https://www.tensorflow.org/)
* [sklearn](https://scikit-learn.org/stable/index.html)

## Code and Presentation Files
1. [`GitHub Project Repository`](https://github.com/boz-tcm/happiness_atlas)
    
2. [`Jupyter Notebook Project Code`](https://github.com/boz-tcm/happiness_atlas/blob/master/Project_2_Neural_Nets.ipynb)
    
3. [`Project Class Presentation Slides`](https://github.com/boz-tcm/happiness_atlas/blob/master/Project%202_%20The%20Neural%20Nets%20.pdf) 

## Team Information

Group 3 - The Neural Nets

**Team Members**: Nirvana Ganpat, Bryant Beckford, Todd Meier, Stephan Guillaume