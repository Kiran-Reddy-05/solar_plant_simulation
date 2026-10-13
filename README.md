# Solar Plant Simulation

## About the Project

I built this project to create a simple dashboard for monitoring the performance of a solar power plant. The main idea is to bring plant performance, weather conditions, and inverter readings together in one place so that the information is easy to view and understand.

The project uses Django for the backend and HTML, CSS, and JavaScript for the frontend. I also created APIs to provide plant and inverter data to the dashboard.

Currently, the readings are simulated rather than collected from a real solar plant.

## What the Project Does

- Displays plant capacity, active power, and capacity utilization.
- Shows weather information such as temperature, solar irradiance, wind speed, and humidity.
- Provides a separate page to view inverter readings.
- Uses APIs to retrieve plant and inverter data in JSON format.
- Refreshes dashboard readings automatically.
- Handles invalid inverter IDs and API errors.
- Includes an About page with project information and a contact form interface.

## Technologies Used

- Python
- Django
- HTML and CSS
- JavaScript
- JSON APIs
- Git and GitHub

## Project Structure

```text
solar-plant-simulation/
├── manage.py
├── solar_project/
│   ├── settings.py
│   └── urls.py
├── plant/
│   ├── views.py
│   ├── simulator.py
│   ├── templates/
│   │   └── plant/
│   └── static/
│       └── plant/
└── README.md
```

## Running the Project Locally

**1. Clone the repository**

```bash
git clone https://github.com/Kiran-Reddy-05/solar_plant_simulation.git
cd solar_plant_simulation
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install Django**

```bash
python -m pip install django
```

If a `requirements.txt` file is available, install the project dependencies using:

```bash
python -m pip install -r requirements.txt
```

**4. Run database migrations**

```bash
python manage.py migrate
```

**5. Start the development server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Available Pages

- `/` — Plant Overview
- `/inverters/` — Inverter Data
- `/about/` — About the Project

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/api/plant/overview/` | Returns plant overview and weather data |
| `/api/data/inverter/` | Returns readings for all inverters |
| `/api/data/inverter/?id=INV001` | Returns readings for a specific inverter |

The APIs return JSON responses, which are used by the frontend to display the readings.

## What I Learned

While building this project, I worked with Django URL routing, views, JSON responses, and frontend-backend communication. I also learned how JavaScript can fetch data from APIs and update a dashboard, and how to handle invalid requests and unexpected errors.

## Future Improvements

I would like to extend this project by adding historical data storage, performance charts, configurable alerts, and integration with real solar inverter data.


