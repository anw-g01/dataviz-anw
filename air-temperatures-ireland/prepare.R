
library(readr)
library(dplyr)
library(lubridate)
library(stringr)

df <- read_csv(file.path("air-temperatures-ireland", "data", "mth06.csv"))

df <- df %>% 

    # standardise all column names (lower case and with underscores)
    rename_with(
        ~ str_to_lower(
            str_replace_all(., " ", "_")
        )
    ) %>% 
  
    # rename certain columns
    rename(
        # new name = old name
        date = day,
        weather_station = meteorological_weather_station
    ) %>% 
  
    # remove missing values
    filter(
        !is.na(value)
    ) %>% 
  
    # update and create new columns  
    mutate(

        # convert character columns to factors 
        across(
            where(is.character),
            as.factor
        ),

        date = ymd(date),
        datetime = ymd_hms(paste0(date, hour)),

        month_name = factor(
            month(date, label = TRUE, abbr = TRUE),
            levels = month.abb,
            ordered = TRUE
        ),
        weekday = factor(
            wday(date, label = TRUE, abbr = TRUE),
            levels = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
            ordered = TRUE
        ),
        hour = hour(datetime)
    )

# export as RDS file
saveRDS(df, file.path("air-temperatures-ireland", "data", "air-temp-cso-2025.rds"))


