from flask import Flask, request, render_template
import arxiv, string, re, json

app = Flask(__name__)


# index url
@app.route('/')
def index():
    return render_template('index.html')


# requst url
@app.route('/search', methods=['POST'])
def search():
    input_value = request.form.get("value")
    # write into file
    if input_value:
        with open("search-record.txt", "a+") as output_file:
            output_file.write(input_value + '\n')

    data = arxiv.query(search_query=input_value, start=0, max_results=500)
    return json.dumps(data)


@app.route('/monthly/analysis', methods=['GET'])
def analysis():
    return render_template('monthly-analysis.html')


@app.route('/showhistory', methods=['POST'])
def show_history():
    history_list = {}

    with open('./search-record.txt', 'r') as f:
        for item in f.readlines():

            item = item.strip('\n')
            if item not in history_list:
                history_list[item] = 1
            else:
                history_list[item] += 1;

    return json.dumps(history_list)


app.run()
