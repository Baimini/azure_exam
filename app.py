from flask import Flask, request, render_template
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("form.html")

@app.route('/aml', methods=['POST'])
def aml():
    try:
        # 1. 接收前端資料
        # p1 現在代表 SeriousDlqin2yrs (通常是 0 或 1)
        serious_dlq = request.form.get('p1') 
        debt_ratio = request.form.get('p2')
        monthly_income = request.form.get('p3')
        late_90_days = request.form.get('p4')

        # 2. 組裝成 AML 端點所需的格式
        data = {
            "Inputs": {
                "input1": [
                    {
                        "SeriousDlqin2yrs": serious_dlq,
                        "DebtRatio": debt_ratio,
                        "MonthlyIncome": monthly_income,
                        "NumberOfTimes90DaysLate": late_90_days
                    },
                ],
            },
            "GlobalParameters": {}
        }

        # AML 設定 (請填入您的實際資訊)
        url = '你的AML端點URL'
        api_key = '你的API_KEY'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        # 3. 呼叫端點
        response = requests.post(url, data=json.dumps(data), headers=headers)
        result = response.json()

        # 解析結果
        prediction_data = result['Results']['WebServiceOutput0'][0]
        label = str(prediction_data['Scored Labels'])
        # 取得機率 (Scored Probabilities)
        probability = prediction_data.get('Scored Probabilities', '無資料')

        risk_text = "高風險" if label == "1" or label == "1.0" else "低風險"
        
        htmlstr = f"""
        <html>
            <head><title>分析結果</title></head>
            <body>
                <h2>分析結果</h2>
                <p>依據您輸入的參數，此人違約風險結果為：<strong>{risk_text}</strong></p>
                <p>違約機率預測值：{probability}</p>
                <br>
                <a href="/">返回重新輸入</a>
            </body>
        </html>
        """
        return htmlstr

    except Exception as e:
        return f"發生錯誤: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)