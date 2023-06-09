"""   University Recommendation System 
      Advanced Database Topics Project 
      Code By: Anubhav Kumar Rajat, Manak Agarwal, Shruti Chopra, Sudhanshu Parhar
"""

# Importing the required libraries file

from flask import Flask, render_template, escape, request, redirect
import pandas as pd
import numpy as np
from sklearn import neighbors, datasets
from numpy.random import permutation
from sklearn.metrics import euclidean_distances, precision_recall_fscore_support

# importing the UnderGrad Recommendation file
import undergraduateUniveristyRecommendor

# App FLow (HTML file paths from where pages are load)
app = Flask(__name__, static_folder='../Frontend',
            template_folder='../Frontend')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graduateuniversity')
def GraduateUniversity():
    return render_template('graduateuniversity.html')


@app.route('/undergraduateuniversity')
def UndergraduateUniversity():
    return render_template('undergraduateuniversity.html')


@app.route("/main")
def return_main():
    return render_template('index.html')

# Function for calculating the Euclidean Distance


def EucDistance(TrainSet, TestSet, Len):
    Dist = 0
    for i in range(Len):
        Dist = Dist + np.square(TestSet[i]-TrainSet[i])
    DistFinal = np.sqrt(Dist)
    return DistFinal

# Function for K-nearest Neighbour Algorithm - Supervised learning for classification


def KnearestN(TrainDataSet, Test_Input, N):
    DistFinals = {}
    sorted_values = {}
    Len = Test_Input.shape[1]

    for i in range(len(TrainDataSet)):
        DistFinal = EucDistance(Test_Input, TrainDataSet.iloc[i], Len)
        DistFinals[i] = DistFinal[0]

    Sorted_DistFinals = sorted(DistFinals.items(), key=lambda i: i[1])
    print(Sorted_DistFinals[:5])

    nNeighbors = []

    for i in range(N):
        nNeighbors.append(Sorted_DistFinals[i][0])

    RedundNeighbors = {}

    for i in range(len(nNeighbors)):
        NeighCheck = TrainDataSet.iloc[nNeighbors[i]][-1]

        if NeighCheck in RedundNeighbors:
            RedundNeighbors[NeighCheck] = RedundNeighbors[NeighCheck] + 1
        else:
            RedundNeighbors[NeighCheck] = 1
    print(NeighCheck)

    Sort_nNeighbors = sorted(RedundNeighbors.items(),
                             key=lambda i: i[1], reverse=True)
    return(Sort_nNeighbors, nNeighbors)


# Algorithm for Undergraduate Recommendation

@app.route('/undergraduateuniversityinputs')
def UndergraduateUniversityScript():
    EndRes = undergraduateUniveristyRecommendor.main()
    Collec1 = []
    Collec2 = []

    for x in EndRes:
        Collec1.append(x[0])
    for x in EndRes:
        Collec2.append(x[1])
    return '''
<html>
    <head>
        <title>University Recommendation System</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css"
            crossorigin="anonymous">
        <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
    

    </head>
    
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <h3 class="navbar-brand">University Recommendation System</h3>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <div class="navbar-nav">
                    <a href="#" class="btn btn-primary">Home<span class="sr-only">(current)</span></a>
                    <a href="/graduateuniversity" class="btn btn-primary">Graduate University</a>
                    <a href="/undergraduateuniversity" class="btn btn-primary">Undergraduate University</a>
                </div>
            </div>
        </nav>
      <div class="pad" style="padding">
        <div class="main-block">
            <form action="/undergraduateuniversityinputs">
                <div class="title">
                    <i class="fas fa-pencil-alt"></i>
                    <h3>Recommended UnderGraduate Universities List</h3>
                </div>
                <div class="info">
                    <table class="table table-bordered table-dark">
                        <thead>
                            <th scope="col">Sr No</th>
                            <th scope="col">University Name</th>
                            <th scope="col">Acceptance Rate</th>
                        </thead>
                        <tbody>
                            <tr>
                              <th scope="row">1</th>
                              <td>{EndRes10}</td>
                              <td>{EndRes11}</td>
                            </tr>
                            <tr>
                                <th scope="row">2</th>
                                <td>{EndRes20}</td>
                                <td>{EndRes21}</td>
                              </tr>
                              <tr>
                                <th scope="row">3</th>
                                <td>{EndRes30}</td>
                                <td>{EndRes31}</td>
                              </tr>
                              <tr>
                                <th scope="row">4</th>
                                <td>{EndRes40}</td>
                                <td>{EndRes41}</td>
                              </tr>
                              <tr>
                                <th scope="row">5</th>
                                <td>{EndRes50}</td>
                                <td>{EndRes51}</td>
                              </tr>
                          </tbody>
                    </table>
    
                </div>
    
            </form>
        </div>
    
      </div>
        <footer class="footer">
        </footer>
    </body>
</html>         
   '''.format(EndRes10=Collec1[0], EndRes11=Collec2[0], EndRes20=Collec1[1], EndRes21=Collec2[1], EndRes30=Collec1[2], EndRes31=Collec2[2], EndRes40=Collec1[3], EndRes41=Collec2[3], EndRes50=Collec1[4], EndRes51=Collec2[4])


@app.route('/graduateuniversityinputs')
def GraduateUniversityScript():
    Processed_Data = pd.read_csv(
        'C:/Users/mnkgr/OneDrive/Desktop/University Recommendation System/datasets/Processed_data.csv')
    Processed_Data.drop(Processed_Data.columns[Processed_Data.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    greV = float(request.args.get("greV"))
    print(greV)
    greQ = float(request.args.get("greQ"))
    print(greQ)
    greA = float(request.args.get("greA"))
    print(greA)
    cgpa = float(request.args.get("cgpa"))
    print(cgpa)
    TestDataSet = [[greV, greQ, greA, cgpa]]
    TestSet = pd.DataFrame(TestDataSet)
    print(TestSet)
    N = 7
    EndRes, Nearest = KnearestN(Processed_Data, TestSet, N)
    Collec1 = []
    Collec2 = []
    for x in EndRes:
        Collec1.append(x[0])
    for x in EndRes:
        Collec2.append(x[1])
    for x in Collec1:
        print(x)
    return '''
     <html>
            <head>
                <title>University Recommendation System</title>
                
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
               
            </head>
            <body>
                <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <h3 class="navbar-brand">University Recommendation System</h3>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <div class="navbar-nav">
                    <a href="#" class="btn btn-primary">Home<span class="sr-only">(current)</span></a>
                    <a href="/graduateuniversity" class="btn btn-primary">Graduate University</a>
                    <a href="/undergraduateuniversity" class="btn btn-primary">Undergraduate University</a>
                </div>
            </div>
        </nav>

 <div class="main-block">
            
            <form action="/undergraduateuniversityinputs">
                <div class="title">
                    <i class="fas fa-pencil-alt"></i>
                    <h3>Recommended Graduate Universities List</h3>
                </div>
                <div class="info">
                    <table class="table table-bordered table-dark">
                        <thead>
                            <th scope="col">Sr No</th>
                            <th scope="col">University Name</th>
                            
                        </thead>
                        <tbody>
                            <tr>
                              <th scope="row">1</th>
                              <td>{EndRes10}</td>
                              
                            </tr>
                            <tr>
                                <th scope="row">2</th>
                                <td>{EndRes20}</td>
                               
                              </tr>
                              <tr>
                                <th scope="row">3</th>
                                <td>{EndRes30}</td>
                               
                              </tr>
                              <tr>
                                <th scope="row">4</th>
                                <td>{EndRes40}</td>
                               
                              </tr>
                              <tr>
                                <th scope="row">5</th>
                                <td>{EndRes50}</td>
                               
                              </tr>
                          </tbody>
                    </table>
    
                </div>
    
            </form>
        </div>                   
                    <footer class="footer">
                    </footer>
                </div>
            </body>
        </html>
    '''. format(EndRes10=Collec1[0], EndRes20=Collec1[1], EndRes30=Collec1[2], EndRes40=Collec1[3], EndRes50=Collec1[4])


if __name__ == '__main__':
    app.run()
