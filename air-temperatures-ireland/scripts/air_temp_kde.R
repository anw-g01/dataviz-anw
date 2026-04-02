
library(ggplot2)
library(geomtextpath)
library(ggtext)

df <- readRDS(file.path("air-temperatures-ireland", "data", "air-temp-cso-2025.rds"))

# plot: kernel density estimate (KDE) 
df <- df %>% 
    group_by(date) %>% 
    summarise(avg_temp = mean(value)) %>% 
    ggplot(
        aes(
            x = avg_temp
        )
    ) + 
    
    # KDE plot with curved station text labels
    geom_density(
        aes(
            y = after_stat(count)
        ),     
        adjust = 0.9,
        linewidth = 0.7,
        colour = "#BB1544FF",
        fill = "#BB1544FF",
        alpha = 0.1
    ) +
        
    # x and y axis settings
    scale_x_continuous(n.breaks = 10) +
    scale_y_continuous(n.breaks = 5) +
    coord_cartesian(
        clip = "off"
    ) +
  
    # labels
    labs(
        title = "<b>Distribution of Daily Air Temperature in Ireland 2025</b>",
        subtitle = "Kernel density estimate of daily <b>air temperatures</b>",
        caption = "Data: Central Statistics Office (CSO), Ireland – Air Temperature (2025)",
        x = "Temperature (°C)", 
        y = NULL    
    ) +
    
    # base theme
    theme_minimal(
        base_family = "Palatino Linotype",
        base_size = 11   
    ) +
  
    # theme adjustments
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
        axis.title.x = element_text(margin = margin(t = 9)),
        # panel.grid.major.y = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text.x = element_text(
            vjust = 0.5,
            colour = "black",
            size = rel(1.2)
        ),
        legend.position = "none",
        plot.margin = margin(15, 15, 15, 15)
    )

ggsave(
    file.path("air-temperatures-ireland", "images", "air_temp_kde.svg"),
    height = 6, 
    width = 9
)
