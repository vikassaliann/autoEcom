# 📈 Automated E-Commerce Price Tracker 📉

This is a full-stack web application that allows users to track product prices from e-commerce websites. Users can add a product by its URL, set a target price, and the system will automatically scrape the site periodically to check for price drops.

The entire application is containerized with Docker for easy setup and deployment.

---
## ✨ Features

* User Authentication (Login/Logout).
* Add, View, and Delete products to track.
* Background web scraping jobs that don't block the user interface.
* Price history logging for each product.
* Automated, hourly price checks initiated by a system cronjob.
* A clean, modern UI provided by the Pico.css framework.

---
## 🛠️ Tech Stack

* **Backend:** Django, Celery, PostgreSQL, Redis
* **Frontend:** HTML, Pico.css
* **Scraping:** Python with Requests & BeautifulSoup
* **Orchestration:** Docker, Docker Compose, RabbitMQ
* **Automation:** Cronjob

---
## ✅ Prerequisites

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

---
## 🚀 Getting Started

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Build and Run the Docker Containers**
    This command builds and starts all the services (Django, Postgres, Celery, etc.) in the background.
    ```bash
    docker-compose build
    docker-compose up -d
    ```

3.  **Set Up the Database and Admin User**
    Run the following commands to initialize the database and create your admin account.
    ```bash
    # Apply database migrations
    docker-compose exec app python manage.py migrate

    # Create a superuser for logging in
    docker-compose exec app python manage.py createsuperuser
    ```
    Follow the prompts to create your username and password.

---
## 💻 Usage

1.  **Access the Web App:** Open your browser and go to **http://localhost:8000**.

2.  **Log In:** Use the superuser credentials you just created.

3.  **Track Products:** Use the form to add product URLs and your desired target price. The first scrape will be triggered immediately.

**Important:** The web scraper in `tracker/tasks.py` is configured with CSS selectors for Amazon by default. If you want to track products from a different website, you must **inspect that site's HTML** and update the selectors in the `scrape_product_price` task.

---
## ⚙️ Setting Up Automation (Cronjob)

The final step is to create a system cronjob that will automatically check the prices of all tracked products every hour.

1.  Open your system's crontab for editing:
    ```bash
    crontab -e
    ```

2.  Add the following line to the file. **Remember to replace the path** with the absolute path to your project directory.

    ```
    # Run the price checker every hour for the autoecom project
    0 * * * * cd /path/to/your/project/autoecom && docker-compose exec app python manage.py check_prices >> /path/to/your/project/autoecom/cron.log 2>&1
    ```

3.  Save and close the editor. The automation is now live!
