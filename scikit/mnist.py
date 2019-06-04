import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
import numpy as np
import pandas as pd

digit = datasets.load_digits()

images_and_lables = list(zip(digit.images, digit.target))
for index, (image, label) in enumerate(images_and_lables[:4]):
    plt.subplot(2, 4, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title("Training: %i" % label)
    # plt.show()

n_sample = len(digit.images)
data = digit.images.reshape((n_sample, -1))

classifier = svm.SVC(gamma=0.001)
classifier.fit(data[:n_sample // 2], digit.target[:n_sample // 2])

expected = digit.target[n_sample // 2 :]
predicted = classifier.predict(data[n_sample // 2:])

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

image_and_predictions = list(zip(digit.images[n_sample // 2 :], predicted))
for index, (image, label) in enumerate(image_and_predictions[:4]):
    plt.subplot(2, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title("Training: %i" % label)
    plt.show()

if __name__ == '__main__':
    print()