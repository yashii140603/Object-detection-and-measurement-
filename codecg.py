import cv2

def measure_objects(image_path, reference_length_cm):
    # Load the image from the file
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load image.")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to create a binary image
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No contours found in the image.")

    # Assume the second largest contour is the reference object
    contours_sorted = sorted(contours, key=cv2.contourArea, reverse=True)
    reference_contour = contours_sorted[1]  # Second largest contour
    ref_x, ref_y, ref_w, ref_h = cv2.boundingRect(reference_contour)

    # Calculate the pixel-to-centimeter ratio using the reference object's known length
    reference_length_px = max(ref_w, ref_h)
    pixel_per_cm = reference_length_px / reference_length_cm

    # Process each contour to measure dimensions
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Calculate dimensions in centimeters
        object_width_cm = w / pixel_per_cm
        object_height_cm = h / pixel_per_cm

        # Draw the bounding box and the dimensions on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(image, f'{object_width_cm:.2f}cm x {object_height_cm:.2f}cm', 
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 2) 

    # Scale down the image for display
    scale_factor = 0.4
    resized_image = cv2.resize(image, (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor)))

    # Show the result
    cv2.imshow('Measured Objects', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = r'D:\CAMBRIDGE COLLEGE NOTES\6th SEMESTER\CG Mini Project\Code\vscCG1\7.jpeg'
reference_length_cm = 5.0  # Length of the reference object in centimeters
measure_objects(image_path, reference_length_cm)


image_path = r'D:\CAMBRIDGE COLLEGE NOTES\6th SEMESTER\CG Mini Project\Code\vscCG1\1.jpeg'
reference_length_cm = 5.0  # Length of the reference object in centimeters
measure_objects(image_path, reference_length_cm)

image_path = r'D:\CAMBRIDGE COLLEGE NOTES\6th SEMESTER\CG Mini Project\Code\vscCG1\5.jpeg'
reference_length_cm = 5.0  # Length of the reference object in centimeters
measure_objects(image_path, reference_length_cm)

image_path = r'D:\CAMBRIDGE COLLEGE NOTES\6th SEMESTER\CG Mini Project\Code\vscCG1\6.jpeg'
reference_length_cm = 5.0  # Length of the reference object in centimeters
measure_objects(image_path, reference_length_cm)




