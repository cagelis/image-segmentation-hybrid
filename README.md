
# Hybrid Image Segmentation with Superpixels and Region Growing

This project implements a hybrid approach to image segmentation, combining SLIC superpixels and region growing. It was developed as a **team project** for the university course *Digital Image Processing* at the University of Thessaly.

## Project Description

The goal of this project is to simplify and improve image segmentation by:
- First applying **SLIC superpixels** to reduce the image to compact regions of similar texture and color.
- Then using a **region growing** algorithm to merge adjacent superpixels based on color similarity in the LAB color space.

This combination results in clearer, more meaningful segments while reducing computational complexity.

## Technologies Used

- Python 3
- `scikit-image`
- `OpenCV`
- `NumPy`
- `Matplotlib`

## Example Results

Below are example outputs of the segmentation process using different parameter configurations:

### Superpixel Segmentation (SLIC)
![Superpixels](images/project_img_page_7.png)

### Region Growing Output
![Region Growing](images/project_img_page_15.png)

### Effect of Different Parameters
![Example 1](images/project_img_page_16.png)
![Example 2](images/project_img_page_17.png)
![Example 3](images/project_img_page_18.png)
![Example 4](images/project_img_page_19.png)

## Team

This project was developed by a group of students at the University of Thessaly:

- **Christos Agelis** (cangelis@uth.gr)  
- Giorgos Kanakis (gekanakis@uth.gr)  
- Rigas Panagiotopoulos (ripanagiot@uth.gr)  
- Giannis Patas (iopatas@uth.gr)

## How to Run

1. Install dependencies:
```bash
pip install scikit-image opencv-python numpy matplotlib
```

2. Run the Python file:
```bash
python FinalProject2025.py
```

## License

This project is for academic purposes only.
