from flask import Flask, render_template
from signal_processing.plot_update import plot_update
from signal_processing.plt_nrl import plt_fft

#передаёт название файла, который и есть
app = Flask(__name__)

# Главная страница
@app.route('/')
def home():
    return render_template('home.html')

# Генерация сигналов
@app.route('/signal-generation')
def signal_generation():
    return render_template('signal_generation.html')

# Фильтры
@app.route('/filters')
def filters():
    return render_template('filters.html')

# Нейронка
@app.route('/neural')
def neural():
    return render_template('neural.html')


# Обновление графиков
@app.route('/plot_update', methods=['POST'])
def plot():
    return plot_update()

@app.route('/plot_neural', methods=['POST'])
def plot_neural():
    return plt_fft()


#Вывод ошибок, после конца разработки отключить
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)