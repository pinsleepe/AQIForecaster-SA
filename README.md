# AQIForecaster-SA

1. AQIDataFetcher

    Responsibilities:
        Fetch AQI data from AQICN or other data sources.
        Handle API requests and responses.
        Manage API authentication and rate limiting.
    Methods:
        get_current_aqi(): Fetch current AQI data.
        get_historical_aqi(): Fetch historical AQI data for model training.
        get_forecast_data(): Fetch forecast data for specific pollutants.

2. DataProcessor

    Responsibilities:
        Parse and clean the fetched data.
        Prepare data for analysis and model input.
        Feature engineering, such as creating lag features and datetime features.
    Methods:
        parse_json(): Convert JSON data into a structured format.
        create_features(): Generate features useful for the prediction model.

3. ModelTrainer

    Responsibilities:
        Train predictive models with historical AQI data.
        Validate model performance using historical data.
        Persist trained models for future use.
    Methods:
        train_model(): Train a model on the historical data.
        evaluate_model(): Evaluate model accuracy and performance.
        save_model(): Save the trained model to disk.
        load_model(): Load a model from disk.

4. ForecastPredictor

    Responsibilities:
        Use trained models to make AQI predictions.
        Incorporate forecast data into the prediction process.
    Methods:
        predict_aqi(): Predict future AQI based on model and forecast inputs.
        format_prediction_output(): Format predictions for presentation or further analysis.

5. APIManager (Optional)

    Responsibilities:
        Abstract the complexity of interacting with external APIs.
        Manage different endpoints and their specific requirements.
    Methods:
        make_request(): Make requests to external APIs.
        handle_response(): Process API responses.

6. ConfigManager

    Responsibilities:
        Manage configuration settings for the package, such as API keys, endpoints, and model parameters.
    Methods:
        load_config(): Load configuration from a file or environment variables.
        get_config_value(): Retrieve specific configuration values.

# Data
[Maitland Historical Data URL](https://aqicn.org/historical/#city:south-africa/maitland)

# TODO

1. Save pulled current data JSON files.
2. Deal with "KeyError: 'timestamp'" 