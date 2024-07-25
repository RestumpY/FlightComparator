# test_function.R

# Définir une fonction de test
#* @get /test
function() {
  list(msg = "Service plumber fonctionne correctement")
}

# Définir une fonction de prédiction
#* @param class_encoded:int
#* @param duration:int
#* @get /predict
predict_price <- function(class_encoded, duration) {
  # Ajouter des logs pour le débogage
  cat("class_encoded:", class_encoded, "\n")
  cat("duration:", duration, "\n")
  
  # Créer le dataframe d'entrée avec les noms corrects
  input_data <- data.frame(class_encoded = as.numeric(class_encoded), duration = as.numeric(duration))
  
  # Ajouter des logs pour vérifier le dataframe
  cat("input_data:\n")
  print(input_data)
  
  # Effectuer la prédiction avec gestion des erreurs
  tryCatch({
    prediction <- predict(model, input_data)
    cat("prediction:", prediction, "\n")
    return(list(prediction = prediction))
  }, error = function(e) {
    # Log the error message
    cat("Error in prediction:", e$message, "\n")
    return(list(error = e$message))
  })
}
