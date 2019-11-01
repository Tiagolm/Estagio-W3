import matplotlib.pyplot as plt
import matplotlib.dates as date
import matplotlib
import datetime
import io
import base64
 
def build_graph(x_coordinates, y_coordinates, tip, x_label, y_label, label_plotagem):
    matplotlib.rcParams['figure.figsize'] = 14, 6.45
    img = io.BytesIO()
    converted_dates = list(map(datetime.datetime.strptime, x_coordinates, len(x_coordinates)*['%d/%m/%Y']))
    x_axis = converted_dates
    formatter = date.DateFormatter('%d/%m/%Y')
    plt.plot(x_axis, y_coordinates, tip, label=label_plotagem)
    ax = plt.gcf().axes[0] 
    ax.xaxis.set_major_formatter(formatter)
    plt.gcf().autofmt_xdate(rotation=90)
    plt.legend()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)