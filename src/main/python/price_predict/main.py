import numpy as np
import copy as copy
import pandas as pd
import math as math
import matplotlib.pyplot as plt
from mysql.connector import (connection)
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

'''
Cria a conexão com banco de dados
'''
cnx = connection.MySQLConnection(user='root', password='fernandok4',
                                 host='127.0.0.1',
                                 database='marketcap')

'''
Crio um array de forma a: dataX é os valores anteriores na serie temporal e o dataY é o 
resultado, ou seja, o preço de fechamento da ação... Faço isso pois quero prever o preço do dia
subsequente utilizando os dados do dia anterior...
'''
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset) - look_back):
		a = dataset[i : (i + look_back), 1:7]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 5])
	return np.array(dataX), np.array(dataY)

'''
faço um select na tabela em que gravei os dados historicos
'''
dataframe = pd.read_sql('SELECT dt_trade, vl_min, vl_max, vl_variation, vl_open, vl_close, qt_volume ' 
                        + ' FROM tb_instrument_history_cotation WHERE id_instrument = 1 AND qt_volume <> 0'
                        + ' ORDER BY dt_trade', con=cnx)

'''
Instancio um scaler para normalizar os dados de 0 a 1 que é o recomendado quando tratamos de
redes neurais e inteligencia artificial... Existem alguns tipos de normalizadores:
    
    - MinMaxScaler: Transforma os valores entre 0 e 1... sendo o maior 1 e o menor 0... Utiliza a formula:
        x = (x' - min) / (max - min)
'''
scaler = MinMaxScaler(feature_range=(0, 1))
# normalizo somente os dados que forem numericos
dataframe[['vl_min', 'vl_max', 'vl_variation', 'vl_open', 'vl_close', 'qt_volume']] = scaler.fit_transform(dataframe[['vl_min', 'vl_max', 'vl_variation', 'vl_open', 'vl_close', 'qt_volume']])
dataset = dataframe.values

'''
Aqui estou pegando o tamanho do meu array e determinando o que será treinamento
e o que será usado para teste (não entrará no treinamento)... No caso determinei que
95% da base de dados será utilizado para treinar e o restante será para o teste.
'''
train_size = int(len(dataset) * 0.95)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

'''
Pre-processo os dados de maneira a criar um novo array de forma a conter os dados do dia anterior
em trainX que corresponde aos resultados do dia em trainY... Faço isso para analisar os impactos no resultado
conforme o dia anterior de pregão.
'''
trainX, trainY = create_dataset(train, 1)
testX, testY = create_dataset(test, 1)

'''
Estou transformando os formatos de ambas as variaveis que são uma matriz de 3 dimensões,
fazendo y virar z e vice-versa... é necessário já que a entrada do meu modelo será y e z onde y
vai ter 6 colunas e z é uma linha
'''
trainX = np.reshape(trainX, (trainX.shape[0], 6, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 6, testX.shape[1]))

'''
Aqui instancio o meu modelo, assim como treino da rede neural... Eai fui testando aqui, por exemplo,
quando dou model.add(Dense(12)), estou adicionando uma camada oculta em que todos os neuronios se comunicam
com o anterior... O 12 é a quantidade de neuronios... Como estamos trabalhando com rede neural recorrente
escolhi o modelo de memória de longo prazo, portanto, crio através do Sequential(Sequential([LSTM(6, input_shape=(6, 1))]))
indicando que essa camada tem 6 neuronios e a minha entrada vai ser uma matriz de 6 por 1...
A otimização coloquei para usar o erro quadratico medio... e o otimizador é adam (existem diversos
otimizadores para experimentar)... e logo depois passo o treinamento
'''
model = Sequential([LSTM(6, input_shape=(6, 1))])
model.add(Dense(12))
model.add(Dense(12))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=30, batch_size=1, verbose=2)

'''
Aqui fiz um esquema para ter o formato da entrada e da saida, isso porque posteriormente, vou querer
fazer o inverso da scaller que usamos no inicio do codigo, eai precisamos ter o mesmo formato que
foi passado na primeira vez e ele tinha 6 
'''
trainPredictFormat = np.zeros(shape=(len(trainX), 6) )
testPredictFormat = np.zeros(shape=(len(testX), 6) )

trainPredict = copy.copy(trainPredictFormat)
trainPredict[:, 4] = np.reshape(model.predict(trainX), (trainX.shape[0]))

testPredict = copy.copy(testPredictFormat)
testPredict[:, 4] = np.reshape(model.predict(testX), (testX.shape[0]))

'''
Aqui inverto o scaller que usamos, para ter a predição no valor real e não na escala de 0 e 1
'''
# invert predictions
finalTrainPredictFormat = scaler.inverse_transform(trainPredict)
finalTrainPredictY = copy.copy(trainPredictFormat)
finalTrainPredictY[:, 4] = finalTrainPredictFormat[:, 4]
finalTrainY = copy.copy(trainPredictFormat)
finalTrainY[:, 4] = trainY
finalTrainY = scaler.inverse_transform(finalTrainY)


finalTestPredictFormat = scaler.inverse_transform(testPredict)
finalTestPredictY = copy.copy(testPredictFormat)
finalTestPredictY[:, 4] = finalTestPredictFormat[:, 4]
finalTestY = copy.copy(testPredictFormat)
finalTestY[:, 4] = testY
finalTestY = scaler.inverse_transform(finalTestY)

'''
Aqui pego os resultados do treino
'''
predictTrainResult = finalTrainPredictY[:, 4]
predictTestResult = finalTestPredictY[:, 4]
trainY = finalTrainY[:, 4]
testY = finalTestY[:, 4]

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY, predictTrainResult))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY, predictTestResult))
print('Test Score: %.2f RMSE' % (testScore))

'''
gero o grafico de preços de fechamento
'''
plt.plot(predictTestResult)
plt.plot(testY)
plt.savefig('data1sequential6dense12dense12dense1.png')
