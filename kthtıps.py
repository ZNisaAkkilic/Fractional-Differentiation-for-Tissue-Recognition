# -*- coding: utf-8 -*-
"""kthtıps.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14KxUiZ67n-5CQYOynMmdwNpElHEvBBLJ
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def load_kth_tips_dataset(data_path, target_size=(128, 128)):


    images = []
    labels = []
    label_names = []

    # Loop through each class directory
    for class_idx, class_name in enumerate(sorted(os.listdir(data_path))):
        class_path = os.path.join(data_path, class_name)

        # Skip if not a directory
        if not os.path.isdir(class_path):
            continue

        label_names.append(class_name)
        print(f"Loading class: {class_name}")


        for img_name in os.listdir(class_path):
            if img_name.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                img_path = os.path.join(class_path, img_name)

                try:

                    img = Image.open(img_path).convert('L')


                    img = img.resize(target_size, Image.Resampling.LANCZOS)


                    img = np.array(img) / 255.0

                    images.append(img)
                    labels.append(class_idx)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")


    images = np.array(images)
    labels = np.array(labels)

    print(f"Dataset loaded: {len(images)} images from {len(label_names)} classes")
    print(f"Image shape: {images[0].shape}")

    return images, labels, label_names


def display_samples(images, labels, label_names, num_samples=5):
    """Display sample images from each class"""
    unique_labels = np.unique(labels)
    plt.figure(figsize=(15, 3*len(unique_labels)))

    for i, label in enumerate(unique_labels):
        indices = np.where(labels == label)[0][:num_samples]
        for j, idx in enumerate(indices):
            plt.subplot(len(unique_labels), num_samples, i*num_samples + j + 1)
            plt.imshow(images[idx], cmap='gray')
            plt.title(f"{label_names[label]}")
            plt.axis('off')
    plt.tight_layout()
    plt.show()


data_path = '/content/drive/MyDrive/KTH-TIPS'


images, labels, label_names = load_kth_tips_dataset(data_path)


display_samples(images, labels, label_names)

import numpy as np
from scipy import special
from scipy.signal import convolve2d

def fractional_derivative_kernel(size, order):

    if size % 2 == 0:
        size = size + 1

    half = size // 2
    k = np.arange(-half, half + 1)


    coeff = np.zeros_like(k, dtype=float)
    for i in range(len(k)):
        coeff[i] = (-1)**i * special.binom(order, i)


    kernel_x = coeff.reshape(1, -1)
    kernel_y = coeff.reshape(-1, 1)

    return kernel_x, kernel_y

def apply_fractional_derivative(image, order, kernel_size=5):

    kernel_x, kernel_y = fractional_derivative_kernel(kernel_size, order)


    dx = convolve2d(image, kernel_x, mode='same', boundary='symm')
    dy = convolve2d(image, kernel_y, mode='same', boundary='symm')


    magnitude = np.sqrt(dx**2 + dy**2)

    return magnitude

def extract_texture_features(images, orders=[0.2, 0.5, 0.8, 1.0]):

    n_samples = len(images)
    n_features = len(orders)
    features = np.zeros((n_samples, n_features))

    for i, img in enumerate(images):
        if i % 100 == 0:
            print(f"Processing image {i}/{n_samples}")

        for j, order in enumerate(orders):

            fd_img = apply_fractional_derivative(img, order)

            features[i, j] = np.mean(fd_img)

    return features


print("Extracting texture features...")
features = extract_texture_features(images)
print("Feature extraction complete!")


X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)

print(f"Training set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns


print("Training SVM classifier...")
clf = SVC(kernel='rbf', random_state=42)
clf.fit(X_train, y_train)


y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = clf.score(X_test, y_test)
print(f"\nAccuracy: {accuracy*100:.2f}%")


cm = confusion_matrix(y_test, y_pred)


plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_names,
            yticklabels=label_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()


print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=label_names))


orders = [0.2, 0.5, 0.8, 1.0]
plt.figure(figsize=(10, 6))
feature_means = np.mean(features, axis=0)
plt.bar(orders, feature_means)
plt.xlabel('Fractional Derivative Order')
plt.ylabel('Average Feature Value')
plt.title('Average Feature Values for Different Fractional Orders')
plt.show()


def visualize_fractional_derivatives(image, orders=[0.2, 0.5, 0.8, 1.0]):
    plt.figure(figsize=(15, 3))


    plt.subplot(1, 5, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original')
    plt.axis('off')


    for i, order in enumerate(orders):
        fd_img = apply_fractional_derivative(image, order)
        plt.subplot(1, 5, i+2)
        plt.imshow(fd_img, cmap='gray')
        plt.title(f'Order {order}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()


print("\nVisualizing fractional derivatives for sample images:")
unique_labels = np.unique(labels)
for label in unique_labels[:3]:
    idx = np.where(labels == label)[0][0]
    print(f"\nClass: {label_names[label]}")
    visualize_fractional_derivatives(images[idx])

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns


scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)


print("Performing 5-fold cross-validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(rf_classifier, X_scaled, labels, cv=cv)

print(f"\nCross-validation scores: {cv_scores}")
print(f"Average CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")


rf_classifier.fit(X_scaled, labels)


orders = [0.2, 0.5, 0.8, 1.0]
plt.figure(figsize=(10, 6))
importances = rf_classifier.feature_importances_
plt.bar(orders, importances)
plt.xlabel('Fractional Derivative Order')
plt.ylabel('Feature Importance')
plt.title('Feature Importance by Fractional Order')
plt.show()


y_pred_full = rf_classifier.predict(X_scaled)
cm = confusion_matrix(labels, y_pred_full)

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd',
            xticklabels=label_names,
            yticklabels=label_names)
plt.title('Confusion Matrix (Random Forest)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()


class_accuracy = cm.diagonal() / cm.sum(axis=1)
plt.figure(figsize=(12, 6))
sns.barplot(x=label_names, y=class_accuracy)
plt.title('Accuracy per Texture Class')
plt.xticks(rotation=45)
plt.ylabel('Accuracy')
plt.tight_layout()
plt.show()


print("\nDetailed Classification Report:")
print(classification_report(labels, y_pred_full, target_names=label_names))


def find_challenging_pairs(cm, class_names):
    n_classes = len(class_names)
    mistakes = []
    for i in range(n_classes):
        for j in range(n_classes):
            if i != j:
                mistakes.append((class_names[i], class_names[j], cm[i,j]))

    mistakes.sort(key=lambda x: x[2], reverse=True)
    return mistakes[:5]

print("\nMost challenging texture pairs (True -> Predicted, Count):")
challenging_pairs = find_challenging_pairs(cm, label_names)
for true_class, pred_class, count in challenging_pairs:
    print(f"{true_class} -> {pred_class}: {count}")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from skimage.feature import hog
from skimage import exposure
import seaborn as sns

def visualize_texture_analysis(image, label_name):

    plt.figure(figsize=(15, 10))


    plt.subplot(3, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title(f'Original Texture\n({label_name})')
    plt.axis('off')


    orders = [0.2, 0.5, 0.8, 1.0]
    for idx, order in enumerate(orders):
        fd_img = apply_fractional_derivative(image, order)
        plt.subplot(3, 3, idx + 2)
        plt.imshow(fd_img, cmap='jet')
        plt.title(f'Fractional Derivative\nOrder {order}')
        plt.axis('off')


    fd_image = apply_fractional_derivative(image, 0.5)
    hog_features, hog_image = hog(
        fd_image,
        orientations=8,
        pixels_per_cell=(16, 16),
        cells_per_block=(1, 1),
        visualize=True
    )

    plt.subplot(3, 3, 6)
    plt.imshow(hog_image, cmap='jet')
    plt.title('HOG Features')
    plt.axis('off')


    plt.subplot(3, 3, 7)
    feature_values = [np.mean(apply_fractional_derivative(image, order)) for order in orders]
    plt.bar(orders, feature_values)
    plt.title('Feature Values\nat Different Orders')
    plt.xlabel('Fractional Order')
    plt.ylabel('Mean Value')

    plt.tight_layout()
    plt.show()


def split_data_with_visualization():

    X = features
    y = labels


    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)


    plt.figure(figsize=(10, 5))
    plt.pie([len(y_train), len(y_val), len(y_test)],
            labels=['Training (60%)', 'Validation (20%)', 'Test (20%)'],
            autopct='%1.1f%%',
            colors=['lightblue', 'lightgreen', 'pink'])
    plt.title('Dataset Split Distribution')
    plt.show()

    return X_train, X_val, X_test, y_train, y_val, y_test


def print_feature_extraction_summary():
    print("\nFeature Extraction Methods Summary:")
    print("-" * 50)
    print("1. Fractional Differentiation:")
    print("   - Orders used:", [0.2, 0.5, 0.8, 1.0])
    print("   - Feature type: Mean intensity of derivative response")
    print("   - Advantages: Captures texture at different scales")
    print("\n2. HOG Features:")
    print("   - Parameters: 8 orientations, 16x16 pixels per cell")
    print("   - Feature type: Gradient orientation histograms")
    print("   - Advantages: Captures local shape and texture patterns")


print("Performing comprehensive analysis...")


X_train, X_val, X_test, y_train, y_val, y_test = split_data_with_visualization()


sample_idx = np.random.choice(len(images))
sample_image = images[sample_idx]
sample_label = label_names[labels[sample_idx]]
visualize_texture_analysis(sample_image, sample_label)


print_feature_extraction_summary()


accuracy_train = rf_classifier.score(X_train, y_train)
accuracy_val = rf_classifier.score(X_val, y_val)
accuracy_test = rf_classifier.score(X_test, y_test)

print("\nModel Performance:")
print(f"Training Accuracy: {accuracy_train:.3f}")
print(f"Validation Accuracy: {accuracy_val:.3f}")
print(f"Test Accuracy: {accuracy_test:.3f}")