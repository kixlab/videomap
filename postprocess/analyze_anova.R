library(tidyverse)
library(jsonlite)
library(FSA)

setwd("/Users/JuhoonLee/Desktop/videomap/postprocess/data/analysis")

# Talking/Non-talking
# talking
talking_vids = list('mZZJYDfmgeg', '1oiCLxngvBo', 'PyWZYHy17As', 'Nu_By3eTpoc', 'u00iLnvVgFc', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', '0SMzqWV6xxs', 'nnzPJv5XIws', 'ZORD4y7dL08', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'VDMOFa8iRqo', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', '5ywy531EMNA', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'A_qivvTkijw', 'S0luUzNRtq0', 'HFp5uH12wkc', 'ynmdOz_D1R4', 'r6JmI35r5E8', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'mwpb65gm1e0', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho', '8DgsLNa3ums', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'XFYHIg8U--4', '1dALzTPQWJg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'b2EZggyT5O4')
# non talking
non_talking_vids = list('XN3N5K2axpw', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'ZeVRqW2J3UY', '_Yb6xLqvsf0', '-szevr-BRZE', 'KLLqGcgxQEw', 'dJ_qCDWNvXU', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', '5AU2vJU-QJM', 'yYOysPt5gic', 'ta5IB2wy6ic', 'rqBiByEbMHc', 'sM81wJ7GDrI', 'djvLEfwwQPU', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'AnWGek4P_dY', 'k0koOhfXv_s', '4WaXJs9RR3E', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'N3c81EPZ51Q', 'Df9F8ettY8k', 'm0H56KpKLHA', 'ygRQRgR11Zg', 'UriwETsgsqg', 'z1Xv6Pa0toE', '1Ni8KOzRzuI', 'yu-G9kEKdTo', 'oe7Cz-dxSBY')

### task type ###
# 82
create = list('mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'nnzPJv5XIws', '-szevr-BRZE', 'KLLqGcgxQEw', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '5AU2vJU-QJM', 'yYOysPt5gic', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', 'ta5IB2wy6ic', '5ywy531EMNA', 'sM81wJ7GDrI', '1Ni8KOzRzuI', 'sij_wNj0doI', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'AnWGek4P_dY', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'oe7Cz-dxSBY', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', 'N3c81EPZ51Q', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'bxXXCP0AE5A', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'XFYHIg8U--4', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'UriwETsgsqg', 'b2EZggyT5O4')
# 27
fix = list('1oiCLxngvBo', 'PyWZYHy17As', '2OoebJA2mnE', '-xCtbeecgKQ', 'z1Xv6Pa0toE', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', 'ZORD4y7dL08', 'Czi_ZirnzRo', 'BzxPDw6ezEc', 'yu-G9kEKdTo', 'tb1L7Rsm1U8', 'mwpb65gm1e0', 'zMqzjMrxNR0', '0fxL8v2dMho', '8DgsLNa3ums', 'e3StC_4qemI', 'ntYwKXN82QU', '2xXPSfQBP-w', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'mj1Fu3-XQpI')
# 11
use = list('u00iLnvVgFc', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'rqBiByEbMHc', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'BotYnPhByWg', 'djvLEfwwQPU', 'wvC3_Rs4mXs', 'CdZQF4DDAxM')

### categories ###
ane = list('mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '1oiCLxngvBo', 'ZT1dvq6yacQ', 'PyWZYHy17As', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'u00iLnvVgFc')
cnov = list('2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', 'z1Xv6Pa0toE', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk')
cne = list('0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'ZORD4y7dL08', '-szevr-BRZE', 'KLLqGcgxQEw', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc')
enc = list('Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M')
fne = list('yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '5AU2vJU-QJM', 'yYOysPt5gic', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s')
health = list('ta5IB2wy6ic', 'rqBiByEbMHc', '5ywy531EMNA', 'sM81wJ7GDrI', '0TLQg_b1v5Q', '1Ni8KOzRzuI', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU')
hnc = list('A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo')
hnt = list('Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'AnWGek4P_dY', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E')
hng = list('tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'mwpb65gm1e0', 'oe7Cz-dxSBY', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho')
pcns = list('8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc')
pna = list('Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs')
snf = list('XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4')


# Read through all the files
filenames <- list.files(pattern="*.json", recursive=TRUE)
df_section <- data.frame()
df_category <- data.frame()
df_type <- data.frame()

task = ""
for (file in filenames) {
  data <- fromJSON(file)

  # Get the section and the portion of each video
  # Section (Time)
  results_section <- data$time_portion$sections %>% enframe('section', 'sectionInfo')
  df <- results_section %>%
    mutate(portion = sectionInfo %>% map_dbl("portion"))
  df <- df[-c(2)]
  vid_id <- gsub(".*/", "", file)
  vid_id <- gsub(".json*", "", vid_id)
  df["style"] <- ifelse(vid_id %in% talking_vids, "talking", "non-talking")
  df["audio"] <- ifelse(vid_id %in% talking_vids, "talking", "non-talking")
  
  if (vid_id %in% create) {
    task = "create"
  }
  else if (vid_id %in% fix) {
    task = "fix"
  }
  else {
    task = "use"
  }
    
  df["task"] <- task
  df["genre"] <- gsub("/.*", "", file)
  df <- select(df, style, audio, task, genre, section, portion)
  df_section <- rbind(df_section, df)
  
  
  
  # Category (Time)
  results_category <- data$time_portion$categories %>% enframe('category', 'categoryInfo')
  df2 <- results_category  %>%
    mutate(portion = categoryInfo %>% map_dbl("portion"))
  df2 <- df2[-c(2)]
  vid_id <- gsub(".*/", "", file)
  vid_id <- gsub(".json*", "", vid_id)
  df2["style"] <- ifelse(vid_id %in% talking_vids, "talking", "non-talking")
  df2["audio"] <- ifelse(vid_id %in% talking_vids, "talking", "non-talking")
  
  if (vid_id %in% create) {
    task = "create"
  }
  else if (vid_id %in% fix) {
    task = "fix"
  }
  else {
    task = "use"
  }
  
  df2["task"] <- task
  df2["genre"] <- gsub("/.*", "", file)
  df2 <- select(df2, style, audio, task, genre, category, portion)
  df_category <- rbind(df_category, df2)
  
  
  # Type (Time)
  results_type <- data$time_portion$types %>% enframe('type', 'typeInfo')
  df3 <- results_type  %>%
    mutate(portion = typeInfo %>% map_dbl("portion"))
  df3 <- df3[-c(2)]
  vid_id <- gsub(".*/", "", file)
  vid_id <- gsub(".json*", "", vid_id)
  df3["style"] <- ifelse(vid_id %in% talking_vids, "talking", "non-talking")
  df3["audio"] <- ifelse(vid_id %in% talking_vids, "talking", "non-talking")
  
  if (vid_id %in% create) {
    task = "create"
  }
  else if (vid_id %in% fix) {
    task = "fix"
  }
  else if (vid_id %in% use) {
    task = "use"
  }
  else {
    task = "screen"
  }
  
  df3["task"] <- task
  df3["genre"] <- gsub("/.*", "", file)
  df3 <- select(df3, style, audio, task, genre, type, portion)
  df_type <- rbind(df_type, df3)
  
}

# aov2 <- aov(portion ~ category*section, data=df_section)
# summary(aov2)
# TukeyHSD(aov2)

# Data

df_section_kruskal_intro <- df_section[df_section$section == "intro", ]
df_section_kruskal_procedure <- df_section[df_section$section == "procedure", ]
df_section_kruskal_outro <- df_section[df_section$section == "outro", ]
df_section_kruskal_misc <- df_section[df_section$section == "misc.", ]

df_category_kruskal_greeting <- df_category[df_category$category == "greeting", ]
df_category_kruskal_overview <- df_category[df_category$category == "overview", ]
df_category_kruskal_step <- df_category[df_category$category == "step", ]
df_category_kruskal_supplementary <- df_category[df_category$category == "supplementary", ]
df_category_kruskal_explanation <- df_category[df_category$category == "explanation", ]
df_category_kruskal_description <- df_category[df_category$category == "description", ]
df_category_kruskal_conclusion <- df_category[df_category$category == "conclusion", ]
df_category_kruskal_misc <- df_category[df_category$category == "misc.", ]

df_type_kruskal_opening <- df_type[df_type$type == "opening", ]
df_type_kruskal_goal <- df_type[df_type$type == "goal", ]
df_type_kruskal_motivation <- df_type[df_type$type == "motivation", ]
df_type_kruskal_briefing <- df_type[df_type$type == "briefing", ]
df_type_kruskal_subgoal <- df_type[df_type$type == "subgoal", ]
df_type_kruskal_instruction <- df_type[df_type$type == "instruction", ]
df_type_kruskal_tool <- df_type[df_type$type == "tool", ]
df_type_kruskal_tip <- df_type[df_type$type == "tip", ]
df_type_kruskal_warning <- df_type[df_type$type == "warning", ]
df_type_kruskal_justification <- df_type[df_type$type == "justification", ]
df_type_kruskal_effect <- df_type[df_type$type == "effect", ]
df_type_kruskal_status <- df_type[df_type$type == "status", ]
df_type_kruskal_context <- df_type[df_type$type == "context", ]
df_type_kruskal_tool_spec <- df_type[df_type$type == "tool specification", ]
df_type_kruskal_closing <- df_type[df_type$type == "closing", ]
df_type_kruskal_outcome <- df_type[df_type$type == "outcome", ]
df_type_kruskal_reflection <- df_type[df_type$type == "reflection", ]
df_type_kruskal_side_note <- df_type[df_type$type == "side note", ]
df_type_kruskal_self_promo <- df_type[df_type$type == "self-promo", ]
df_type_kruskal_bridge <- df_type[df_type$type == "bridge", ]
df_type_kruskal_filler <- df_type[df_type$type == "filler", ]


# Kruskal Test

## 1. Narration

# kruskal.test(portion ~ style, df_section_kruskal_intro)
# kruskal.test(portion ~ style, df_section_kruskal_procedure)
# kruskal.test(portion ~ style, df_section_kruskal_outro)
# kruskal.test(portion ~ style, df_section_kruskal_misc)

# kruskal.test(portion ~ style, df_category_kruskal_greeting)
# kruskal.test(portion ~ style, df_category_kruskal_overview)
# kruskal.test(portion ~ style, df_category_kruskal_step)
# kruskal.test(portion ~ style, df_category_kruskal_supplementary)
# kruskal.test(portion ~ style, df_category_kruskal_explanation)
# kruskal.test(portion ~ style, df_category_kruskal_description)
# kruskal.test(portion ~ style, df_category_kruskal_conclusion)
# kruskal.test(portion ~ style, df_category_kruskal_misc)

# kruskal.test(portion ~ style, df_type_kruskal_opening)
# kruskal.test(portion ~ style, df_type_kruskal_goal)
# kruskal.test(portion ~ style, df_type_kruskal_motivation)
# kruskal.test(portion ~ style, df_type_kruskal_briefing)
# kruskal.test(portion ~ style, df_type_kruskal_subgoal)
# kruskal.test(portion ~ style, df_type_kruskal_instruction)
# kruskal.test(portion ~ style, df_type_kruskal_tool)
# kruskal.test(portion ~ style, df_type_kruskal_tip)
# kruskal.test(portion ~ style, df_type_kruskal_warning)
# kruskal.test(portion ~ style, df_type_kruskal_justification)
# kruskal.test(portion ~ style, df_type_kruskal_effect)
# kruskal.test(portion ~ style, df_type_kruskal_status)
# kruskal.test(portion ~ style, df_type_kruskal_context)
# kruskal.test(portion ~ style, df_type_kruskal_tool_spec)
# kruskal.test(portion ~ style, df_type_kruskal_closing)
# kruskal.test(portion ~ style, df_type_kruskal_outcome)
# kruskal.test(portion ~ style, df_type_kruskal_reflection)
# kruskal.test(portion ~ style, df_type_kruskal_side_note)
# kruskal.test(portion ~ style, df_type_kruskal_self_promo)
# kruskal.test(portion ~ style, df_type_kruskal_bridge)
# kruskal.test(portion ~ style, df_type_kruskal_filler)


## 2. Task Type

# kruskal.test(portion ~ task, df_section_kruskal_intro)
# kruskal.test(portion ~ task, df_section_kruskal_procedure)
# kruskal.test(portion ~ task, df_section_kruskal_outro)
# kruskal.test(portion ~ task, df_section_kruskal_misc)


# kruskal.test(portion ~ task, df_category_kruskal_greeting)
# kruskal.test(portion ~ task, df_category_kruskal_overview)
# kruskal.test(portion ~ task, df_category_kruskal_step)
# kruskal.test(portion ~ task, df_category_kruskal_supplementary)
# kruskal.test(portion ~ task, df_category_kruskal_explanation)
# kruskal.test(portion ~ task, df_category_kruskal_description)
# kruskal.test(portion ~ task, df_category_kruskal_conclusion)
# kruskal.test(portion ~ task, df_category_kruskal_misc)

# 
# kruskal.test(portion ~ task, df_type_kruskal_opening)
# kruskal.test(portion ~ task, df_type_kruskal_goal)
# kruskal.test(portion ~ task, df_type_kruskal_motivation)
# kruskal.test(portion ~ task, df_type_kruskal_briefing)
# kruskal.test(portion ~ task, df_type_kruskal_subgoal)
# kruskal.test(portion ~ task, df_type_kruskal_instruction)
# kruskal.test(portion ~ task, df_type_kruskal_tool)
# kruskal.test(portion ~ task, df_type_kruskal_tip)
# kruskal.test(portion ~ task, df_type_kruskal_warning)
# kruskal.test(portion ~ task, df_type_kruskal_justification)
# kruskal.test(portion ~ task, df_type_kruskal_effect)
# kruskal.test(portion ~ task, df_type_kruskal_status)
# kruskal.test(portion ~ task, df_type_kruskal_context)
# kruskal.test(portion ~ task, df_type_kruskal_tool_spec)
# kruskal.test(portion ~ task, df_type_kruskal_closing)
# kruskal.test(portion ~ task, df_type_kruskal_outcome)
# kruskal.test(portion ~ task, df_type_kruskal_reflection)
# kruskal.test(portion ~ task, df_type_kruskal_side_note)
# kruskal.test(portion ~ task, df_type_kruskal_self_promo)
# kruskal.test(portion ~ task, df_type_kruskal_bridge)
# kruskal.test(portion ~ task, df_type_kruskal_filler)


# By Narration
# dunnTest(portion ~ style, df_category_kruskal_step, method="bonferroni")
# dunnTest(portion ~ style, df_category_kruskal_description, method="bonferroni")

# dunnTest(portion ~ style, df_type_kruskal_instruction, method="bonferroni")
# dunnTest(portion ~ style, df_type_kruskal_justification, method="bonferroni")
# dunnTest(portion ~ style, df_type_kruskal_effect, method="bonferroni")
# dunnTest(portion ~ style, df_type_kruskal_tool_spec, method="bonferroni")
# dunnTest(portion ~ style, df_type_kruskal_outcome, method="bonferroni")


# By Task Type
# dunnTest(portion ~ task, df_section_kruskal_misc, method="bonferroni")

# dunnTest(portion ~ task, df_category_kruskal_description, method="bonferroni")
# dunnTest(portion ~ task, df_category_kruskal_misc, method="bonferroni")

dunnTest(portion ~ task, df_type_kruskal_status, method="bonferroni")
dunnTest(portion ~ task, df_type_kruskal_context, method="bonferroni")
dunnTest(portion ~ task, df_type_kruskal_side_note, method="bonferroni")




