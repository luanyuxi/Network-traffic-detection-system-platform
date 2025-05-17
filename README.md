# **Nexora - Real-Time Traffic Awareness System**

## **Description**
Nexora is a traffic monitoring system designed for real-time traffic analysis. It allows users to select datasets, run various machine learning models, and visualize results in an interactive dashboard. The system provides tools to compare model performance, view dataset details, and explore related analytics. It is aimed at users in the domain of traffic analysis, cybersecurity, and machine learning.

## **Features**
- **Dashboard**: A comprehensive dashboard displaying system statistics and data sources.
- **Model Results**: Compare the performance of machine learning models, including accuracy, precision, recall, and F1-score.
- **Dataset Selection**: Choose datasets to train models and visualize data distributions.
- **User Interaction**: View data and model details in an easy-to-navigate interface, including data file descriptions and file download options.
- **Avatar Functionality**: Click on the user avatar to view user details and enlarge the profile image.
- **Visualizations**: Interactive charts and graphs, including t-SNE scatter plots and bar charts to display model metrics.

## **Technology Stack**
- **Frontend**: 
  - Vue.js 3
  - Element Plus (UI components)
  - Vite (Build tool)
  - ECharts (Data visualization)
- **Backend**: 
  - FastAPI (Backend framework)
  - Python (for machine learning and data processing)
- **Machine Learning**:
  - Fuzzy rules (Model training)
  - XGBoost (Gradient boosting model)
  - Random Forest (Ensemble learning)
- **Others**: 
  - Node.js (for development and build)
  - Git (Version control)

## **Installation Instructions**

### 1. **Clone the Repository**
First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/nexora.git
cd nexora
````

### 2. **Install Backend Dependencies**

Ensure you have Python 3.8 or higher installed on your system.

To install the backend dependencies, navigate to the backend folder and run:

```bash
cd backend
pip install -r requirements.txt
```

### 3. **Install Frontend Dependencies**

Make sure Node.js is installed on your system.

Navigate to the frontend folder and install the necessary packages using:

```bash
cd frontend
npm install
```

### 4. **Run the Application**

Once all dependencies are installed, follow the steps below to start the application:

* **Start Backend**:
  Start the backend API server using Uvicorn. From the `backend` directory, run:

  ```bash
  cd backend
  uvicorn main:app --reload
  ```

* **Start Frontend**:
  For the frontend development server, use the following command in the `frontend` directory:

  ```bash
  cd frontend
  npm run dev
  ```

Now, you can visit the application at [http://localhost:3000](http://localhost:3000) to see it in action.

```

This version gives a detailed and structured overview of how to clone the repository, install dependencies for both the frontend and backend, and run the application locally.
```
