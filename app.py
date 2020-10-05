from wtforms.fields.core import FieldList, SelectField
from wtforms.widgets.core import TextArea
from graphmaker.maker import make_graph, make_file
from flask import Flask, json, request, jsonify, render_template, send_file
from wtforms import Form, BooleanField, StringField, validators, IntegerField, widgets, FormField
import pandas as pd
from random import randint, shuffle
from io import BytesIO, StringIO
app = Flask(__name__)


class Graph_form(Form):
    id_key = StringField('Id key', default='id', validators=[
                         validators.Length(min=1, max=25)])
    x_axis = StringField('X axis key', default='key', validators=[
                         validators.Length(min=1, max=25)])
    y_axis = StringField('Y axis key', default='value', validators=[
                         validators.Length(min=1, max=25)])
    hue_key = StringField('Hue (farge) key', default='time', validators=[
                          validators.Length(min=1, max=25)])

    yellow_hline = IntegerField('Yellow hline', validators=[
            validators.Optional(),
            validators.NumberRange(min=-999999, max=999999)
        ])

    red_hline=IntegerField('Red hline', validators=[
        validators.Optional(),
        validators.NumberRange(min=-999999, max=999999)
        ])

    excel_field=StringField('Excel Paste', widget=TextArea(), default='id\tvalue\ttime\tkey\n1\t71\tt1\tsos\n2\t62\tt1\temo\n3\t82\tt1\thyp\n4\t73\tt2\tsos\n5\t94\tt2\temo\n6\t52\tt2\thyp')

class Rcads_q(Form):
    text = StringField('Text')
    score = IntegerField('Score', validators=[validators.NumberRange(min=0,max=5)])

class Rcads_form(Form):
    age = IntegerField(default=99)
    qs = FieldList(FormField(Rcads_q))
    #qs = FieldList(IntegerField('score'), min_entries=6)


class Pre_questionnaire_form(Form):
    age = IntegerField(default=99)
    questionnaire = SelectField('sdq, Eiberg or RCADS', choices=['SDQ','RCADS','Eiberg'])
    shuffle_list = ['0']*20+['1']*20+['2']*5+['3']*2
    shuffle(shuffle_list)
    excel_field=StringField('Excel Paste', widget=TextArea(), default='\t'.join(shuffle_list))
    #inline_form = FormField()


@ app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/pre', methods=['GET', 'POST'])
def pre_q_form():
    form = Pre_questionnaire_form(request.form)
    if request.method == 'POST' and form.validate():
        generated_form = Rcads_form()
        generated_form.age.data = form.age.data
        scores = form.excel_field.data.split('\t')
        with app.open_resource('static/items.txt') as f:
            questiontexts = [byteline.decode('utf-8') for byteline in f.read().split(b'\n')]
        for score, text in zip(scores, questiontexts):
            scoreForm = Rcads_q()
            scoreForm.score.data=score
            scoreForm.text.data=str(text)
            generated_form.qs.append_entry(data=scoreForm.data)
        return render_template('rcads.html', form = generated_form)
    else:
        return render_template('preforms.html', form=form)
    


def json_to_svg(df, settings=None):
    #print('json to svg')
    #print(request.form)
    fig=make_graph(data=df, settings=settings)
    fig_file=make_file(fig=fig)
    return fig_file


@ app.route('/simple',  methods=['GET', 'POST'])
def excelpaste():
    form=Graph_form(request.form)

    if request.method == 'POST' and form.validate():
        excel_string=form.excel_field.data
        settings=form.data

        string_IO=StringIO(excel_string)
        df=pd.read_csv(string_IO, sep='\t')
        svg=json_to_svg(df, settings)
        return svg.getvalue()
    elif request.method == 'GET':
        return render_template('test.html', form=form)
    else:
        return render_template('test.html', form=form), 400


@ app.route('/rcads', methods=['GET', 'POST'])
def single_items():
    form = Rcads_form(request.form)
    if request.method == 'POST' and form.validate():
        sorted_qs = json.load(open('static/sorted_qs.json'))
        top_problems_id = [i for i,q in enumerate(form.data['qs']) if q['score'] >= 2]
        my_sorted_qs = [[topic[0], []] for topic in sorted_qs]

        for i, topic in enumerate(sorted_qs):
            for q in topic[1]:
                if q[0] in top_problems_id:
                    my_sorted_qs[i][1].append(q[1])

        return render_template('top_problems.html', top_problems=my_sorted_qs)
    else:
        return render_template('rcads.html', form=form)

@app.route('/questionsexample')
def example():
    return render_template('example.html')

if __name__ == '__main__':
    app.run()
