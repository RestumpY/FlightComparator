library(plumber)
library(randomForest)

# Charger le modèle
model <- readRDS("random_forest_model.rds")

# Charger les fonctions définies dans test_function.R
r <- plumb("test_function.R")

# Démarrer le service plumber
r$run(port=8000)
