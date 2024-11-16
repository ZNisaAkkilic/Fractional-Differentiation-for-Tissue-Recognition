Fractional Differentiation for Tissue Recognition
Overview
This project focuses on tissue recognition using advanced image processing techniques, specifically employing fractional differentiation and Histogram of Oriented Gradients (HOG) for feature extraction. The approach enhances traditional image analysis by utilizing fractional derivatives at various orders, which allows for capturing subtle textural information in tissues, making it more effective for classification and recognition tasks.

Features
Fractional Differentiation:

Utilizes fractional derivatives to extract detailed features from tissue images at different scales (orders: 0.2, 0.5, 0.8, 1.0).
Captures both fine and coarse texture patterns by varying the fractional order.
HOG (Histogram of Oriented Gradients):

Computes gradient orientation histograms of fractional derivative images.
Captures local shape and texture patterns in the tissue images.
Visualization:

Comprehensive visualization of the original image, fractional derivatives, HOG features, and feature distributions at different fractional orders.
Data Splitting:

The dataset is split into training (60%), validation (20%), and testing (20%) sets.
Visualizes the distribution of the data across these sets.
Model Performance:

Implements a machine learning classifier (e.g., Random Forest) for tissue classification.
Tracks and reports model performance on training, validation, and test datasets.
Installation
To run this project, you need to install the required libraries. You can do so using pip:


pip install -r requirements.txt
Make sure to have Python 3.x installed on your machine.

Usage
Clone the repository:


git clone https://github.com/yourusername/fractional-differentiation-tissue-recognition.git
cd fractional-differentiation-tissue-recognition
Import and use the functions in your own project or directly run the script for analysis:


# Example usage
from texture_analysis import visualize_texture_analysis, split_data_with_visualization
The main analysis functions:

visualize_texture_analysis(image, label_name): Visualizes the original image, fractional derivatives, HOG features, and feature distributions.
split_data_with_visualization(): Splits the dataset into training, validation, and testing sets and visualizes the distribution.
print_feature_extraction_summary(): Prints a summary of the feature extraction methods used in the project.
For performance evaluation, simply run the script or the main function which will output the model's training, validation, and testing accuracy.

Example Results
After running the analysis, you will see:

A visual representation of the tissue image alongside its fractional derivatives at different orders.
The HOG feature visualization.
A bar chart displaying feature values at different fractional orders.
A pie chart representing the data split distribution.
Additionally, the model's accuracy on the training, validation, and test datasets will be printed.

Feature Extraction Summary
Fractional Differentiation:

Orders used: [0.2, 0.5, 0.8, 1.0]
Captures texture at different scales.
Measures the mean intensity of derivative responses to capture finer details in tissue images.
HOG Features:

Parameters: 8 orientations, 16x16 pixels per cell.
Features: Gradient orientation histograms that help in understanding local shape and texture patterns.
Model Evaluation
The Random Forest classifier is used to evaluate tissue recognition.
The accuracy for training, validation, and testing datasets is computed and displayed.
Requirements
Python 3.x
Libraries:
numpy
matplotlib
scikit-learn
scipy
scikit-image


