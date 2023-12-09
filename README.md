# Installation Guide

Follow these steps to install the required dependencies:

1. **Install Python**: Ensure you have Python installed on your system. If not, you can download it from [here](https://www.python.org/downloads/).

2. **Install Required Packages**: Install the required packages using pip, which is a package manager for Python. Open your terminal and run the following command:
    ```bash
    pip install -r requirements.txt
    ```
3. **Update pip (if necessary)**: If you encounter any issues during installation, your pip version might be outdated. You can update pip using the following command:
    ```bash
    python -m pip install --upgrade pip
    ```
4. **Create a Virtual Environment (Optional)**: It's recommended to create a virtual environment to keep the dependencies required by different projects separate. You can create a virtual environment using the following command:
    ```bash
    python -m venv venv
    ```
5. **Activate the Virtual Environment**: Before you can start installing or using packages in the virtual environment, you'll need to activate it. You can do this using the following command:
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```
6. **Install Required Packages in the Virtual Environment**: Now you can install the required packages in the virtual environment by running the following command:
    ```bash
    pip install -r requirements.txt
    ```

# To do List
- [X] User Login and Registration
- [X] Admin Registration
- [X] Display All Movies
- [ ] Display a Movie
  - [X] Show Movie Information
  - [ ] Show Cast with their Roles
  - [ ] Show the Movie Reviews and Rating
  - [ ] Restructure the models to use id for better url routing
- [ ] View a Cast Member
  - [ ] Show the Cast Member Profile
  - [ ] Show Cast Member's Filmography
- [ ] View a Director
  - [ ] Show the Director's Information
  - [ ] Show the Director's Filmography
- [ ] View a Genre
  - [ ] Make Genres into Tags
  - [ ] Show movies all movies in the Genre
- [ ] Search Button
  - [ ] Add Button to Navigation Bar 
  - [ ] Add filters


