# Load required packages
library(dplyr)
library(stringdist)
library(ggplot2)
library(stats)
library(randomForest)
library(tidyr)
library(broom)
library(readxl)

# Example data frames
survey <- read_excel("Documents/thesis/survey.xlsx")
flanker <- read_excel("Documents/thesis/flanker.xlsx")

# Convert ID columns to lowercase
survey <- survey %>%
  mutate(IDkoda = tolower(IDkoda))

flanker <- flanker %>%
  mutate(subjectId = tolower(subjectId))

# Function to find the best match for an ID from another dataframe with a threshold
find_best_match <- function(id, candidate_ids, threshold = 0.2) {
  distances <- stringdist::stringdist(id, candidate_ids, method = "jw")  # Jaro-Winkler distance
  # Filter matches based on the threshold
  if (min(distances) <= threshold) {
    candidate_ids[which.min(distances)]
  } else {
    NA
  }
}

# Apply the fuzzy matching function to find best matches
flanker <- flanker %>%
  rowwise() %>%
  mutate(best_match = find_best_match(subjectId, survey$IDkoda, threshold = 0.2)) %>%
  ungroup()

# Define the list of weird matches to exclude
weird_matches <- data.frame(
  subjectId = c("123janb", "abds321", "lili123", "eeee123", "slar100", "mers123"),
  best_match = c("123abcd", "abcd123", "heli123", "pete123", "sl10", "test123"),
  stringsAsFactors = FALSE
)

# Filter out the weird matches from the result
filtered_results <- flanker %>%
  anti_join(weird_matches, by = c("subjectId", "best_match"))

# Join the tables based on the filtered results
result <- filtered_results %>%
  left_join(survey, by = c("best_match" = "IDkoda"))

result <- result %>% filter(!is.na(best_match))

# Identify and filter out exact matches
non_exact_matches <- result %>%
  filter(subjectId != best_match, !is.na(best_match))

# View the non-exact matches
print(non_exact_matches)

v<- non_exact_matches[c(1,13)]

survey$IDkoda<- tolower(survey$IDkoda)
flanker$subjectId <- tolower(flanker$subjectId)
df_joined <- inner_join(survey ,flanker, by = c( "IDkoda"="subjectId" ))

write.xlsx(df_joined, "df_joined.xlsx")
write.xlsx(result, "result.xlsx")