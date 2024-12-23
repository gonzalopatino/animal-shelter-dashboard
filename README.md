# Animal Shelter Dashboard

## Project Overview
This project involves the development of an interactive dashboard for managing and visualizing animal shelter data. The dashboard enables filtering, geolocation mapping, and breed distribution analysis for rescued animals. Built using Python, MongoDB, and the Dash framework, this project ensures a user-friendly interface and robust backend for maintaining the data.

## Features and Functionality
- **Interactive Filters**: Filter animals based on rescue types (Water, Mountain, or Disaster) or reset the filters. Filters dynamically update the data table, pie chart, and geolocation map.
- **Dynamic Map**: Displays the geolocation of selected animal records.
- **Pie Chart Visualization**: Displays breed distribution for selected filters.
- **Data Table**: A scrollable table presenting detailed animal records, allowing single-row selection to update the map and pie chart.

## Tools Used
- **Python**: Backend programming and MongoDB integration.
- **MongoDB**: Storage and querying of animal shelter data.
- **Dash Framework**: Application logic and interactive visualizations.
- **Plotly**: Dynamic pie chart generation for breed distribution.
- **Dash Leaflet**: Geolocation mapping features.

## Why These Tools Were Selected
### MongoDB
- **Flexible Schema**: Accommodates unstructured animal attributes.
- **Python Integration**: Seamless interaction via PyMongo.
- **Scalability**: Handles large datasets efficiently.

### Dash Framework
- **Ease of Use**: Integrates backend logic with front-end visualizations.
- **Interactivity**: Supports dynamic updates for charts, maps, and filters.

### Dash Leaflet
- **Geolocation Features**: Simplifies the addition of map-based interactivity.

## Steps to Reproduce
1. **Set Up MongoDB**:
   - Install MongoDB.
   - Create a database named `AAC` with a collection called `animals`.
   - Populate the collection with animal shelter data.

2. **Install Required Libraries**:
   - Install Python libraries such as `dash`, `plotly`, `dash-leaflet`, and `pymongo`.

3. **Run the Dashboard**:
   - Save the Python script and the `crud_operations.py` file in the same directory.
   - Execute the script.

4. **Access the Dashboard**:
   - Open the browser and navigate to `http://127.0.0.1:<port>`.

5. **Interact with the Dashboard**:
   - Test filters, map, and pie chart updates with the dataset.

## Challenges and Solutions
### Challenge 1: Filter Implementation
- **Problem**: Translating MongoDB filter logic to Python queries.
- **Solution**: Developed specific queries within Dash callbacks to dynamically filter the dataset.

### Challenge 2: Blank Names in Records
- **Problem**: Missing names in some records.
- **Solution**: Used "No name found" as a fallback value in the map popups.

### Challenge 3: Map Alignment Issues
- **Problem**: Map pointer failed to update correctly with selected records.
- **Solution**: Debugged callback logic to validate and handle missing geolocation data.

## Reflection and Insights
1. **How do you write programs that are maintainable, readable, and adaptable?**
   - Programs are made maintainable by following coding standards, implementing modular design, and providing clear documentation. For instance, the CRUD Python module created in Project One was reusable and well-documented, which enabled seamless integration with the dashboard widgets in Project Two. This modular approach reduced complexity, simplified debugging, and enhanced adaptability when adding features.

2. **How could this CRUD Python module be used in the future?**
   - The CRUD module could be used in various applications where database interactions are required, such as inventory management, customer relationship systems, or any application involving dynamic data manipulation. Its flexibility makes it suitable for any project requiring structured data operations.

3. **How do you approach problems as a computer scientist?**
   - As a computer scientist, I break down problems into manageable parts. For example, in this project, I started by understanding Grazioso Salvare's database and dashboard requirements. Then, I planned the architecture, focusing on the separation of concerns between the model (MongoDB), view (Dash), and controller (callbacks). This methodical approach ensured all requirements were met efficiently.

4. **How did this project differ from previous assignments?**
   - This project required integrating a front-end dashboard with a back-end database, which was a more holistic task compared to the isolated back-end or front-end assignments in previous courses. It also demanded attention to both technical performance (e.g., handling large datasets) and user experience (e.g., intuitive filters and dynamic visualizations).

5. **What strategies will you use for future database projects?**
   - In future projects, I would:
•	Conduct thorough requirement analysis to design a schema that aligns with client needs.
•	Maintain a modular and well-documented codebase for easy updates and adaptability.


6. **What do computer scientists do, and why does it matter?**
   - Computer scientists design, develop, and optimize systems to solve complex problems and improve efficiency. Their work underpins technological progress across industries. For example, my work on this project helps Grazioso Salvare optimize rescue operations by providing actionable insights, ultimately enhancing their mission's effectiveness.

## Summary
The Grazioso Salvare Dashboard project successfully meets the business and technical requirements outlined in the initial specifications. By leveraging modern technologies such as MongoDB, Dash, and Plotly, the system provides an interactive and user-friendly interface for managing animal shelter data.
The Grazioso Salvare Dashboard demonstrates the power of combining advanced data management (MongoDB) with interactive visualization tools (Dash and Plotly). This project not only fulfills its functional requirements but also lays the foundation for future scalability, such as adding new rescue types, integrating advanced analytics, or expanding database records.



