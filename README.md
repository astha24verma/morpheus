# Form Builder Application

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
The Form Builder application is designed to allow Admins to create forms similar to Google Forms. Admins can create forms with various question types, and users can submit responses anonymously. Both Admins and users can access analytics for each form.

## Features

### Admin User
- **Create Forms:**
  - Create unlimited forms.
  - Add up to 100 questions per form.
  - Select a type for each question (Text, Dropdown, Checkbox).
  - Order questions within a form.
  - Configure question-specific details (e.g., options for dropdown/checkbox).

- **View Forms:**
  - See a list of all forms they have created.

### End User
- **Submit Responses:**
  - Respond to any form anonymously.
  - Submit responses an unlimited number of times.

### Shared Features
- **View Analytics:**
  - Access analytics for every form at a public URL.
  - See total response count at the form level.
  - View question-specific analytics:
    - **Text Field:** Distribution of the top 5 most common words (≥5 characters).
    - **Checkbox:** Distribution of the top 5 option combinations.
    - **Dropdown:** Distribution of the top 5 selected options.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/formbuilder.git
   ```

2. **Navigate into the project directory:**
   ```bash
   cd formbuilder
   ```

3. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser for admin access:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Admin interface: `http://localhost:8000/admin`
   - Form Builder: `http://localhost:8000`

## Usage Guide

### Admin User
- **Creating a Form:**
  - Log in to the admin interface.
  - Navigate to the "Create Form" section.
  - Fill in the form details and add questions.
  - Save the form to make it available for responses.

- **Viewing Forms:**
  - Access the "My Forms" section to see all created forms.
  - Edit or view analytics for each form.

### End User
- **Submitting Responses:**
  - Visit the form URL.
  - Fill in the required fields and submit your response.

### Viewing Analytics
- Access the analytics page for any form to view response data and question-specific insights.

## Code Structure

## Postman Collection

To easily test the API endpoints, you can use our Postman collection. Import the collection into your Postman app using the following link:

[Postman Collection Link](https://astha-lilac-spaceship.postman.co/workspace/Team-Workspace~67d0096c-7a13-4479-8177-1f7fd5968ae9/collection/20726472-760f1867-2ffc-4bbd-95ea-5b18cca8cc2c?action=share&creator=20726472)
