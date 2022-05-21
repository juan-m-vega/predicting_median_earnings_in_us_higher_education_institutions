from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

app = Flask(__name__)

with open('data.pkl', 'rb') as picklefile:
    df_flask = pickle.load(picklefile)

@app.route('/page')
def page():
   return render_template('page.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if request.method == 'POST':

        inputs = request.form
        pell_ever = float(inputs['pell_ever'])
        avgfacsal = np.log(float(inputs['avgfacsal']))
        dep_rpy_1yr_rt = float(inputs['dep_rpy_1yr_rt'])
        private_np = float(df_flask[df_flask['instnm'] == inputs['instnm']]['private_np'])
        med_earnings_growth = float(df_flask[df_flask['instnm'] == inputs['instnm']]['med_earnings_growth'])
        public_pell_ever = float(df_flask[df_flask['instnm'] == inputs['instnm']]['public']) * pell_ever
        high_research_and_grad_log_avgfacsal = float(df_flask[df_flask['instnm'] == inputs['instnm']]['high_research_and_grad']) * avgfacsal
        public_dep_rpy_1yr_rt= float(df_flask[df_flask['instnm'] == inputs['instnm']]['public']) * dep_rpy_1yr_rt
        public_log_cdr2 = float(df_flask[df_flask['instnm'] == inputs['instnm']]['public']) * np.log(float(inputs['cdr2']))
        actual_earnings = round(float(df_flask[df_flask['instnm'] == inputs['instnm']]['md_earn_wne_p6']))
        cdr2 = round(float(df_flask[df_flask['instnm'] == inputs['instnm']]['cdr2']))

        earn_data = np.array([pell_ever,
                             avgfacsal,
                             private_np,
                             dep_rpy_1yr_rt,
                             med_earnings_growth,
                             public_pell_ever,
                             high_research_and_grad_log_avgfacsal,
                             public_dep_rpy_1yr_rt,
                             public_log_cdr2])

        X = df_flask[['pell_ever','log_avgfacsal','private_np','dep_rpy_1yr_rt','med_earnings_growth','public_pell_ever',
                      'high_research_and_grad_log_avgfacsal','public_dep_rpy_1yr_rt','public_log_cdr2']]
        y = df_flask['log_earnings']

        earn_pred = round(np.exp(GradientBoostingRegressor().fit(X,y).predict(earn_data.reshape(1, -1)).astype(float)[0]))

        earn_change = round(earn_pred - actual_earnings)

        pell_ever_actual = round(float(df_flask[df_flask['instnm'] == inputs['instnm']]['pell_ever']))
        avgfacsal_actual = round(float(df_flask[df_flask['instnm'] == inputs['instnm']]['avgfacsal']))
        dep_rpy_1yr_rt_actual = round(float(df_flask[df_flask['instnm'] == inputs['instnm']]['dep_rpy_1yr_rt']))
        cdr2_actual = round(float(df_flask[df_flask['instnm'] == inputs['instnm']]['cdr2']))
        avgfacsal = round(float(inputs['avgfacsal']))
        
        pict = '/static/HigherEducation.jpeg'

        return render_template(
            'page.html', earn_pred = earn_pred,
            actual_earnings = actual_earnings,
            earn_change = earn_change,
            pell_ever_actual = pell_ever_actual,
            avgfacsal_actual = avgfacsal_actual,
            dep_rpy_1yr_rt_actual = dep_rpy_1yr_rt_actual,
            cdr2_actual  = cdr2_actual,
            pell_ever = pell_ever,
            avgfacsal= avgfacsal,
            dep_rpy_1yr_rt = dep_rpy_1yr_rt,
            cdr2  = cdr2)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
