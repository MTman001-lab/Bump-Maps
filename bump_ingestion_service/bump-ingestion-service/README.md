# Bump Ingestion Service

This project is a Bump Ingestion Service that processes bump events from vehicles. It connects to a database to store and manage bump data and utilizes MQTT for event handling.

## Project Structure

```
bump-ingestion-service
├── src
│   ├── main.py          # Entry point of the application
│   ├── db.py            # Database interactions
│   ├── config.py        # Configuration settings
│   └── bump_logic.py     # Core logic for processing bump events
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd bump-ingestion-service
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed. Then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   Update the `src/config.py` file with your database and MQTT broker settings.

4. **Run the application:**
   Execute the following command to start the service:
   ```
   python src/main.py
   ```

## Usage

The service will start ingesting bump events. You can monitor the output in the console. Ensure that your MQTT broker is running and accessible.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.