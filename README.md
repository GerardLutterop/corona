# Corona spread and measures simulation for the Netherlands

Simulation of illness and individual spread of disease.
Approach: model activities and locations per person and compute the spread of the virus, based on the
activities. The model is as realistic and fine-grained as possible, but contains a large number of 
assumptions.  
  The assumptions are translated into code and used to get a more accurate model of the transmission.
The goal is to model all the possble measures and see which measure has the most effect with the least
damage, in human and all other aspects.

# Approach

# Assumptions

There are many (seeming) differences per country in the spread and seriousness of corona. Assumptions 
change all the time, when new knowledge is gained.

## Infection
The virus is transmitted mostly by human contact, by touching hands or coughing. Therefore, vicinity of people
is necessary for transmission. Children (age under 20) seem not to transmit the virus, adults do.
The core of the simulation is contact between people. By 'social distancing' and quarantine the transmission can be
eliminated or minimized.

## Mortality

### Age
The mortality is strongly dependent on age, We currently use this table for mortality vs age:

 Age | Corona Mortality (%) | Regular flu
 ---: | ---: | ---: 
 0-9 | 0% | .01%
 10-19 | 0.2% | .01%
 20-29 | 0.2% | .02%
 30-39 | 0.2% | .02%
 40-49 | 0.4% | .02%
 50-59 | 1.3% | .06%
 60-69 | 3.6% | ~0.4%
 70-79 | 8.0% | 0.83%
 80+   | 14.8% | 0.83%
 
 Compared to a regular flu, this is way more lethal. 
[Business Insider quotes Chinese sources](https://www.businessinsider.nl/coronavirus-death-rate-by-age-countries-2020-3?international=true&r=US)

Also, different mortality for different countries are asserted:

**PRC:**

 PRC Age | Corona Mortality (%) | Infected
 ---: | ---: | ---:
 0-9 | 0% | 1%
 10-19 | 0% | 5.2%
 20-29 | 0% | 28.2%
 30-39 | 0.12% | 10.3%
 40-49 | 0.09% | 14%
 50-59 | 0.4% | 19.2%
 60-69 | 1.4% | 12.4%
 70-79 | 5.3% | 6.4%
 80+   | 9.5% | 3.2% 
Source: [RTL Nieuws](https://www.rtlnieuws.nl/nieuws/nederland/artikel/5058341/jongeren-coronabesmetting-risico-misvatting)

**Italy:**

 Italy Age | Corona Mortality (%)
 ---: | ---: 
 0-9 | 0% 
 10-19 | 0% 
 20-29 | 0% 
 30-39 | 0.3% 
 40-49 | 0.5%
 50-59 | 1.1% 
 60-69 | 3.9% 
 70-79 | 13.4% 
 80-89 | 20.6%  
 90+   | 23.1%  
Source: [Vokskrant, ISS](https://www.epicentro.iss.it/coronavirus/bollettino/Report-COVID-2019_17_marzo-v2.pdf)

### Gender

SEX | DEATH RATE confirmed cases | DEATH RATE all cases
--- | ---: | ---:
Male | 4.7% | 2.8%
Female | 2.8% | 1.7%

Source: [Worldometers.info](https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/)

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

# Sources

## Postcode
[lat/lng per postcode](https://github.com/bobdenotter/4pp)
[Bevolking per postcode](https://www.cbs.nl/nl-nl/maatwerk/2018/49/bevolking-en-huishoudens-4-cijferige-postcode-1-1-2018)
