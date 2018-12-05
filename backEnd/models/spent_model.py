import pandas as pd
import numpy as np
import sklearn.ensemble
import pickle
import os
import lime
import lime.lime_tabular
import datetime

model_filename = 'spent_explainable.sav'
train_filename = 'train_np.npy'


def load_model(model_filename):
	pwd = os.getcwd()
	if pwd.find('model') < 0:
		model_filename = "{}/models/{}" .format(pwd, model_filename)

	return pickle.load(open(model_filename, 'rb'))

def load_train(train_filename):
	pwd = os.getcwd()
	if pwd.find('model') < 0:
		train_filename = "{}/models/{}" .format(pwd, train_filename)

	return np.load(train_filename)


def predict_spent(input_val, loaded_model):
	return loaded_model.predict(input_val)


def get_explainer(loaded_model, input_val):
	spent_data_headers = ['Occupation', 'Marital_Status', 'Product_Category_1', 'Product_Category_2', 'Product_Category_3']
	spent_target_headers = ['Purchase']
	explainer = lime.lime_tabular.LimeTabularExplainer(load_train(train_filename), feature_names=spent_data_headers, class_names=spent_target_headers, categorical_features=np.array([]), verbose=True, mode='regression')
	exp = explainer.explain_instance(input_val[0], loaded_model.predict, num_features=5)
	return exp.as_list()


def get_spent(input_val):
	input_val = input_val.reshape(1,5)
	loaded_model = load_model(model_filename)
	predicted_val = predict_spent(input_val, loaded_model)
	explainer = get_explainer(loaded_model, input_val)
	return predicted_val, explainer

if __name__ == '__main__':
	print("Testing")
	input_val = np.asarray([2, 1, 4, 5, 6])
	input_val = input_val.reshape(1,5)
	start = datetime.datetime.now()
	loaded_model = load_model(model_filename)
	print( datetime.datetime.now() - start )
	start = datetime.datetime.now()
	predict = predict(input_val, loaded_model)
	print( datetime.datetime.now() - start )
	explainer = get_explainer(loaded_model, input_val)
	print(predict)
	print(explainer)
	print( datetime.datetime.now() - start )
