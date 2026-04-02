library(ggplot2)
library(geomtextpath)
library(ggtext)
library(paletteer)
library(forcats)

df <- readRDS(file.path("air-temperatures-ireland", "data", "air-temp-cso-2025.rds"))

# aggregate and summarise data 
df <- df %>% 
    group_by(month_name) %>% 
    summarise(avg_temp = mean(value))

# extract the month with highest avg_temp
top_month <- df %>% 
    slice_max(order_by = avg_temp, n = 1) %>% 
    pull(month_name) %>%      
    as.character()

# get the full month name (match index to built-in month names list)
top_month_full <- month.name[match(top_month, str_sub(month.name, 1, 3))]

# assign fill colours for bars
colours <- paletteer_d("MetBrewer::Austria")     
highlight_colour <- colours[[1]]                

df <- df %>% 
    mutate(bar_colour = if_else(month_name == top_month, highlight_colour, "lightgrey"))

# plot: bar chart
ggplot(
    df, 
    aes(
        x = month_name,
        y = avg_temp
    )
) +
    geom_bar(
        stat = "identity",
        width = 0.8,
        aes(fill = month_name == top_month)
    ) +
    scale_fill_manual(
        values = c(
            "TRUE" = highlight_colour,
            "FALSE" = "lightgrey"
        )
    ) + 
    
    # text labels
    geom_text(
        aes(
            label = round(avg_temp, 1),
            colour = month_name == top_month,
            fontface = ifelse(month_name == top_month, "bold", "plain")
        ),
        size = 5,
        vjust = -1
    ) + 
    scale_colour_manual(
        values = c(
            "TRUE" = highlight_colour,
            "FALSE" = "black"
        )
    ) +
  
    coord_cartesian(clip = "off") +
  
    labs(
        title = str_c(
            "<b><span style='color:", highlight_colour, 
            "; font-weight:bold;'>", top_month_full, "</span>",
            " Sees The Higest Average Temperature</b>"
        ),
        subtitle = "Average air temperature (in °C) by month in Ireland 2025",
        caption = "Data: Central Statistics Office (CSO), Ireland – Air Temperature (2025)",
        x = NULL, y = NULL
    ) +
        
    theme_minimal(
        base_family = "Palatino Linotype",
        base_size = 11
    ) +
  
    theme(
        plot.title = element_markdown(
            size = rel(1.5),
            margin = margin(b = 12)
        ),
        plot.subtitle = element_markdown(
            colour = "#6e6e6e",
            size = rel(1),
            margin = margin(b = 24)
        ),
        plot.caption = element_text(
            colour = "#6e6e6e", 
            size = rel(0.7),
            hjust = 1
        ),
        plot.title.position = "plot",
        panel.grid.major.x = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text.x = element_text(
            vjust = 3.5,
            colour = "black",
            size = rel(1.2)
        ),
        legend.position = "none",
        plot.margin = margin(15, 15, 15, 15)
    )

ggsave(
    file.path("air-temperatures-ireland", "images", "avg_monthly_temp.svg"),
    height = 5, 
    width = 9
)
