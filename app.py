from wtforms.widgets.core import TextArea
from graphmaker.maker import make_graph, make_file
from flask import Flask, json, request, jsonify, render_template, send_file
from wtforms import Form, BooleanField, StringField, validators, IntegerField, widgets
import pandas as pd
from io import BytesIO, StringIO
app = Flask(__name__)


class Graph_form(Form):
    id_key = StringField('Id key', default='id', validators=[
                         validators.Length(min=1, max=25)])
    x_axis = StringField('X axis key', default='key', validators=[
                         validators.Length(min=1, max=25)])
    x_axis = StringField('Y axis key', default='value', validators=[
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

    excel_field=StringField('Excel Paste', widget=TextArea(), default='''id	value	time	key
1	71	t1	sos
2	62	t1	emo
3	82	t1	hyp
4	73	t2	sos
5	94	t2	emo
6	52	t2	hyp''')


@ app.route('/')
def hello_world():
    return 'Hello, World!'


def json_to_svg(df, settings=None):
    #print('json to svg')
    #print(request.form)
    fig=make_graph(data=df, settings=settings)
    fig_file=make_file(fig=fig)
    return fig_file


@ app.route('/excelpaste',  methods=['GET', 'POST'])
def excelpaste():
    form=Graph_form(request.form)

    if request.method == 'POST' and form.validate():
        excel_string=form.excel_field.data
        settings=form.data

        string_IO=StringIO(excel_string)
        df=pd.read_csv(string_IO, sep='\t')
        svg=json_to_svg(df, settings)
        return svg.getvalue()
    else:
        return render_template('test.html', form=form)


if __name__ == '__main__':
    app.run()
