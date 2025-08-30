import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from skimage.segmentation import slic, mark_boundaries
from skimage.color import rgb2lab
from skimage.util import img_as_float
from collections import defaultdict

# Διαβάζουμε την εικόνα
# Χρησιμοποιήθηκαν διάφορες εικόνες και έχει μείνει ο τίτλος cherry ενδεικτικά
image = cv2.imread('./cherry.jpg') 
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_float = img_as_float(image)

# SLIC Superpixels
segments = slic(image_float, n_segments=200, compactness=10, sigma=1, start_label=0)

# Υπολογισμός μέσου χρώματος κάθε superpixel
def compute_superpixel_colors(image_lab, segments):
    superpixel_colors = {}
    for label in np.unique(segments):
        mask = (segments == label)
        color = image_lab[mask].mean(axis=0)
        superpixel_colors[label] = color
    return superpixel_colors

image_lab = rgb2lab(image_float)
superpixel_colors = compute_superpixel_colors(image_lab, segments)

# Εύρεση γειτονικών superpixels
def find_neighbors(segments):
    neighbors = defaultdict(set)
    h, w = segments.shape
    for y in range(h - 1):
        for x in range(w - 1):
            current = segments[y, x]
            right = segments[y, x+1]
            down = segments[y+1, x]
            if current != right:
                neighbors[current].add(right)
                neighbors[right].add(current)
            if current != down:
                neighbors[current].add(down)
                neighbors[down].add(current)
    return neighbors

neighbors = find_neighbors(segments)

# Region growing: συγχώνευση superpixels με παρόμοιο χρώμα
def region_growing(segments, superpixel_colors, neighbors, threshold=15.0):
    new_labels = {}
    current_label = 0
    visited = set()
    label_map = np.full_like(segments, -1)

    for sp in np.unique(segments):
        if sp in visited:
            continue
        stack = [sp]
        group = []

        while stack:
            s = stack.pop()
            if s in visited:
                continue
            visited.add(s)
            group.append(s)

            for n in neighbors[s]:
                if n not in visited:
                    diff = np.linalg.norm(superpixel_colors[s] - superpixel_colors[n])
                    if diff < threshold:
                        stack.append(n)

        for g in group:
            new_labels[g] = current_label
        current_label += 1

    print("Συνολικές περιοχές που δημιουργήθηκαν:", current_label)

    # Δημιουργία του label_map
    for y in range(segments.shape[0]):
        for x in range(segments.shape[1]):
            sp_label = segments[y, x]
            label_map[y, x] = new_labels.get(sp_label, -1)

    return label_map

# Υπολογισμός χρόνου 
start_time = time.time()
label_map = region_growing(segments, superpixel_colors, neighbors, threshold=5.0)
end_time = time.time()

print("Χρόνος εκτέλεσης (Runtime): {:.4f} δευτερόλεπτα".format(end_time - start_time))

# Μετατροπή σε έγχρωμη αναπαράσταση
def label_map_to_color_image(label_map):
    np.random.seed(42)
    unique_labels = np.unique(label_map)
    label_colors = {label: np.random.rand(3,) for label in unique_labels}
    color_image = np.zeros((label_map.shape[0], label_map.shape[1], 3))
    for y in range(label_map.shape[0]):
        for x in range(label_map.shape[1]):
            color_image[y, x] = label_colors[label_map[y, x]]
    return color_image

final_color = label_map_to_color_image(label_map)

# Εμφάνιση αποτελεσμάτων
fig, ax = plt.subplots(1, 4, figsize=(24, 6))
ax[0].imshow(image)
ax[0].set_title('Αρχική εικόνα')
ax[0].axis('off')

ax[1].imshow(mark_boundaries(image, segments))
ax[1].set_title('Superpixels (SLIC)')
ax[1].axis('off')

ax[2].imshow(label_map, cmap='nipy_spectral')
ax[2].set_title('Label Map (Region Growing)')
ax[2].axis('off')

ax[3].imshow(final_color)
ax[3].set_title('Τελική Κατάτμηση (χρώματα)')
ax[3].axis('off')

plt.tight_layout()
plt.savefig("segmentation_results.png")
plt.show()

# Αποθήκευση αρχείων
cv2.imwrite("superpixels_overlay.png", cv2.cvtColor((mark_boundaries(image, segments) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
cv2.imwrite("final_segmentation.png", cv2.cvtColor((final_color * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
