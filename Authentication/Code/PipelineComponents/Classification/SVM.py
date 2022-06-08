from sklearn import svm

class svm_classifier():
    def __init__(self, training_data, labels):
        self.training_data = training_data
        self.labels = labels

        if len(self.training_data) != len(self.labels):
            raise ValueError("Length of inputs does not match the amount of labels")

        self.clf = svm.SVC(kernel="linear").fit(self.training_data, self.labels)

    def predict(self, input):
        return self.clf.predict(input)

if __name__ == '__main__':
    x = [[0,0], [1,1]]
    y = [0, 1]
    SVM = svm_classifier(x, y)
    print(SVM.predict([[2,2]]))