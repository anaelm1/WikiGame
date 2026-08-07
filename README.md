# WikiGame

**Video Demo:** 

**Live Demo:** https://wiki-game-phi.vercel.app/ 

Play a few rounds, and let me know if you enjoyed!!

**Project Link:** https://github.com/anaelm1/WikiGame

![Gameplay Screenshot](./Readme%20pic.PNG)

## Table of Contents
1. [Description](#description)
2. [Technologies Used](#technologies-used)
3. [File Structure](#file-structure)
4. [How to Run Locally](#how-to-run-locally)
5. [Note on the Database](#note-on-the-database)
6. [AI Usage](#ai-usage)
7. [Design Changes](#design-changes)
8. [Future Plans](#future-plans)
9. [License](#license)
10. [Contact Info](#contact-info)

---

## Description
WikiGame is an online game in which you are given a random Wikipedia start page and must reach a designated target page using only the hyperlinks present within the articles. This game is inspired by popular creators who look for creative and unique web-based games, similar to GeoGuessr.

---

## Technologies Used
* **Python and Flask:** Backend server and game logic.
* **SQLite:** Database for storing game records.
* **HTML & CSS:** Frontend design and user interface.

---

## File Structure

### Backend & Configuration
* **[app.py](./app.py):** The main Python file that hosts the Flask server and contains the routing functions for each page (login, index, etc.). It also manages Flask sessions using a cache system.
* **[helper.py](./helper.py):** A secondary Python file used to store non-Flask utility functions. This includes:
  * Fetching Wikipedia titles and pages.
  * Cleaning the pages using Beautiful Soup. This process converts all Wikipedia `href` links into local `/` routes so the user remains inside the game environment.
  * Generating random, popular Wikipedia page titles using Python's `random` module.
  * Converting various title formats into plain text to easily compare winning conditions.
* **[records.db](./records.db):** The main SQLite database containing the `History` table. This table stores the player's name, start page, target page, number of clicks, route taken, and a timestamp. Records are inserted using the CS50 SQL library inside `app.py`.
* **[records.sql](./records.sql):** The SQL code used to generate the schema for the `History` table.
* **[requirements.txt](./requirements.txt):** Contains all the Python dependencies required to run the web application.
* **[vercel.json](./vercel.json):** The configuration file for Vercel hosting.

### Frontend ([templates/](./templates/))
* **[history.html](./templates/history.html):** A developer-only page that displays all database records using Jinja loops. This page is not advertised on the main website.
* **[index.html](./templates/index.html):** The main landing page of the website.
* **[login.html](./templates/login.html):** The user login page.
* **[page.html](./templates/page.html):** Renders the requested Wikipedia article. It uses a GET request to receive the title and calls functions in `helpers.py` to display the content.
* **[won.html](./templates/won.html):** The victory screen that displays all of the player's statistics for that round.

### Other Resources
Included in the repository is a handwritten WikiGame planning PDF created prior to coding. While many details were changed or omitted as the project evolved, it serves as a good representation of the initial project vision. The repository also contains screenshots taken during the development process.

---

## How to Run Locally

To run this project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anaelm1/WikiGame.git
   cd WikiGame
   ```

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   *(If the database isn't automatically created by `app.py`, initialize it manually using the provided SQL file)*
   ```bash
   sqlite3 records.db < records.sql
   ```

5. **Run the Flask application:**
   ```bash
   flask run
   ```
   *The application should now be running locally at `http://127.0.0.1:5000/`.*

---

## Note on the Database
I faced some difficulty during the hosting process on Vercel, as I discovered Vercel does not natively support persistent SQLite databases. To solve this, I set up a conditional system: if the game runs locally, the database works normally. If hosted on Vercel, the database is moved to the `/tmp` folder, which temporarily stores data but resets whenever the serverless function restarts. 

I attempted to implement a cloud database but realized it would require rewriting a significant portion of my existing code. Because of this, I opted to keep the hybrid local/temporary database system for now.

---

## AI Usage
AI tools were utilized during development for the following tasks:
* Designing CSS forms and matching Wikipedia's styling.
* Implementing the Wikipedia API requests system.
* Debugging errors.
* Research purposes (as an alternative to Google Search).
* Formatting this README.

I strictly avoided direct copy-pasting of AI-generated code. All AI tools were configured specifically to guide me rather than provide direct solutions or code blocks.

---

## Design Changes
Initially, I planned to implement an AI (LLM or otherwise) to calculate and display the most optimal path between the start and target pages. However, I had to scrap this plan as pathfinding through Wikipedia requires advanced machine learning skills that fall outside the current scope of this project.

I also planned to include player comparison charts to show how a user's run compared to others who played the exact same route. This proved impossible since the game is not commercialized and lacks a large dataset of player data. Implementing this would also have negatively affected the random nature of page generation.

---

## Future Plans
Although I have closed this project for now, I would love to return to it in the future to implement various quality-of-life features. If I learn machine learning, creating the AI optimal pathfinder will definitely be my first personal project.

---

## License
MIT License

---

## Contact Info
**Anael Mumtaz**  
Karachi, Pakistan  
Email: [anaelmumtaz15@gmail.com](mailto:anaelmumtaz15@gmail.com)  
GitHub: [anaelm1](https://github.com/anaelm1)
