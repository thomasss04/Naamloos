import math
import matplotlib.pyplot as plt
import psycopg2
def lineare_regressie1(listX, listY, itterations, learningrate):
    a = 0
    b = 0
    for i in range(itterations):
        for j in range(len(listX)):
            error = (a + b * listX[j]) - listY[j]
            a = a - error * learningrate * 10000
            b = b - error * learningrate * listX[j]

    print(error, a,b)
    return a, b



def lineare_regressie2(listX, listY, itterations, learningrate):
    a = 0
    b = 0
    for i in range(itterations):
        errorA = 0
        errorB = 0
        SSE = 0
        for j in range(len(listX)):
            errorA = errorA + 2 * a + 2 * b * listX[j] - 2 * listY[j]
            errorB = errorB + 2 * a * listX[j] - 2 * listY[j] * listX[j] + 2 * b * listX[j]**2
            SSE = SSE + ((a + b * listX[j]) - listY[j])**2
        if abs(errorA) > 10:
            a = a - errorA * learningrate
        if abs(errorB) > 100000:
            b = b - min(abs(SSE / errorB), abs(errorB)) * errorB / abs(errorB) * learningrate
    return a, b



connection_string = "host='4.234.56.16' dbname='Steam' user='postgres' password='mggfgg55' port='5432'"
conn = psycopg2.connect(connection_string) # get a connection with the database
cursor = conn.cursor() # a ‘cursor’ allows to execute SQL in a db-session
owners = []
ratio = []
release_date = []
query = """ SELECT appid, name, release_date, positive_ratings, negative_ratings, owners, price
FROM games
WHERE positive_ratings > 0 AND (negative_ratings + positive_ratings > 50)"""
cursor.execute(query)
data = cursor.fetchall()
for game in data:
    ratio.append(((game[-4] / (game[-4] + game[-3])) * game[-2]**(1/32))) # fractie van revieuws dat positief is (0 - 1)
    release_date.append((int(str(game[2])[0:4]) - 1970) * 372 + (int(str(game[2])[5:7]) -1) * 31 + int(str(game[2])[-2:]) -1) # format yyyy-mm-dd naar dagen sinds 1 jan 1970
plt.scatter(release_date, ratio, 0.01)
A, B = lineare_regressie2(release_date, ratio, 10000, 0.000001)
xpoints = [min(release_date), max(release_date)]
ypoints = [A + B * min(release_date), A + B * max(release_date)]
plt.plot(xpoints, ypoints)
plt.show()
