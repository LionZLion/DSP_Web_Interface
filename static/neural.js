const button = document.getElementById("transform");
const sigmaSlider = document.getElementById("sigma_slider");
const sigma_out = document.getElementById("sigma_out");
const message = document.getElementById("message");

setupSlider(sigmaSlider, sigma_out);

function setupSlider(element, out_element) {
    out_element.innerHTML = element.value;
    element.addEventListener('input', function() {
        out_element.innerHTML = this.value;
    })
};


button.addEventListener('click', () => { updateValues() })


function updateValues() {
    updatePlot({
        sigma: parseFloat(sigmaSlider.value),
        phrase: message.value
    })
};

var layout_init = {
    yaxis: { title: {text: 'Амплитуда главной частоты', font: {color: 'white'}} },
    xaxis:{ title: {text: 'Время, с', font: {color: 'white'}} },
    paper_bgcolor: '#444444',
    plot_bgcolor: '#c7c7c7',
    font: {color: 'white'},
    height: 350,
    margin: {l: 50, r: 20, t: 0, b: 40},
    padding: 0,
};

// Инициализация графика
function initPlot(data) {
    var trace = {
        x: data.time,
        y: data.signal,
        mode: 'lines',
        name: 'Сигнал',
        line: {color: '#522685', width: 2},
    };
    Plotly.newPlot('plot', [trace], layout_init);
};

// Обновление графика
function updatePlot(params) {
    fetch('/plot_neural', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        let update_data = {x: [data.time],y: [data.signal]};
        Plotly.update('plot', update_data, layout_init);
        document.getElementById("result").innerHTML = data.encrypt;
    })
    .catch(error => console.error("Error in graph draw", error))
};

// Функция инициализации
function initGraph(params) {
    fetch('/plot_neural', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
    })
    // Получение ответа
    .then(response => response.json())
    .then(data => initPlot(data))
    .catch(error => console.error("Error in graph draw", error));
}

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function(){
    initGraph({sigma: 1, phrase: ' '});
});

window.addEventListener('resize', function() {
    Plotly.relayout('plot', {
        width: document.querySelector('.graphcontainer').clientWidth,
    });
})