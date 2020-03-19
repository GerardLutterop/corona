# Covid-19 simulation for the Netherlands

Simulation of illness and indivisual spread of disease.
Approach: model activities and locations per person and compute the spread of the virus, based on the
activities. The model is as realistic and fine-grained as possible, but contains a large number of 
assumptions.  
  The assumptions are translated into code and used to get a more accurate model of the transmission.
The goal is to model all the possble measures and see which measure has the most effect with the least
damage, in human and all other aspects.

# Approach

# Assumptions

There are many (seeming) differences per country in the spread and seriousness of covid-19. Assumptions 
change all the time, when new knowledge is gained.

## Infection
The virus is transmitted mostly by human contact, by touching hands or coughing. Therefore, vicinity of people
is necessary for transmission. Children (age under 20) seem not to transmit the virus, adults do.
The core of the simulation is contact between people. By 'social distancing' and quarantine the transmission can be
eliminated or minimized.

## Mortality

### Age
The mortality is strongly dependent on age, We currently use this table for mortality vs age:

 Age | Covid-19 Mortality (%) | Regular flu
 ---: | ---: | ---: 
 0-9 | 0% | .01%
 10-19 | 0.2% | .01%
 20-29 | 0.2% | .02%
 30-39 | 0.2% | .02%
 40-49 | 0.4% | .02%
 50-59 | 1.3% | .06%
 60-69 | 3.6% | ~0.4%
 70-79 | 8.0% | 0.83%
 80-   | 14.8% | 0.83%
 
 Compared to a regular flu, this is way more lethal. 
[Business Insider quotes Chinese sources](https://www.businessinsider.nl/coronavirus-death-rate-by-age-countries-2020-3?international=true&r=US)

### Gender

SEX | DEATH RATE confirmed cases | DEATH RATE all cases
--- | ---: | ---:
Male | 4.7% | 2.8%
Female | 2.8% | 1.7%

[Worldometers.info](https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/)

### Pre-existing medical conditions

PRE-EXISTING CONDITION | DEATH RATE confirmed cases | DEATH RATE all cases
--- | ---: | ---:
Cardiovascular disease | 13.2% | 10.5%
Diabetes | 9.2% | 7.3%
Chronic respiratory disease | 8.0% | 6.3%
Hypertension | 8.4% | 6.0%
Cancer | 7.6% | 5.6%
no pre-existing conditions |  | 0.9%

[Worldometers.info](https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/)
