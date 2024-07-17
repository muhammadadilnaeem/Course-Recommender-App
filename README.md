# **Course Recommender App**

This is a Streamlit application that provides personalized course recommendations based on user preferences. The app allows users to select courses they have audited or completed, trains a recommendation model, and generates recommendations for new courses.

https://github.com/user-attachments/assets/63d0e067-6355-46d1-9cbf-a97fc055eb19

## **Features**

- Interactive course selection using a dynamic table
- Model training with feedback at each step
- Personalized course recommendations
- Enhanced UI with emojis, colored headings, and central alignment for a better user experience

## **Installation**

1. **Clone the repository:**
    ```bash
    git clone https://github.com/muhammadadilnaeem/Course-Recommender-App.git
    cd Course-Recommender-App
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv st_env
    st_env\Scripts\activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have the datasets in the `data` folder:**
    ```
    Course-Recommender-App/
    ├── data/
    │   ├── ratings.csv
    │   ├── sim.csv
    │   ├── course_processed.csv
    │   └── courses_bows.csv
    ├── backend.py
    ├── recommender_app.py
    └── requirements.txt
    ```

## **Running the App**

1. **Run the Streamlit app:**
    ```bash
    streamlit run recommender_app.py
    ```

2. **Open your web browser and navigate to:**
    ```
    http://localhost:8501
    ```

## **Code Structure**

- **backend.py:** Contains functions for loading datasets, adding new ratings, and generating course recommendations.
- **recommender_app.py:** The main Streamlit app file. It includes the UI components and integrates the backend functions.

## **Usage**

1. **Select courses you have audited or completed.**
2. **Train the model** using the sidebar options.
3. **Generate course recommendations** by clicking the "Recommend New Courses" button.

## **Customization**

- The app uses emojis and colored headings to enhance the user experience.
- Advanced HTML and CSS are used to style the app.


## Contributing

1. **Fork the repository**
2. **Create a new branch**
3. **Make your changes**
4. **Submit a pull request**

## **License**

This project is licensed under the MIT License.

## **Contact**

For any issues or feature requests, please open an issue on this repository or contact me directly at madilnaeem0@gmail.com.

---
