// Спрятанные ползунки
const width_container = document.getElementById("width-container");
const period_container = document.getElementById("period-container");
const sigma_container = document.getElementById("sigma-container");
// 1 график
const frequency = document.getElementById("frequency_slider");
const freqsample = document.getElementById("frequency_sample");
const chirp_freq = document.getElementById("chirp_slider");
const buttons = document.querySelectorAll(".type_signal");
const is_chirp = document.getElementById("chirp-button");
const dft_button = document.getElementById("dft-button");
const phase_signal = document.getElementById("phase_signal");
// 2 график
const buttons_imp = document.querySelectorAll(".type_impuls");
const fs_imp = document.getElementById("frequency-sample-imp");
const dft_button_imp = document.getElementById("dft-button-imp");
const phase_imp = document.getElementById("phase_imp");
const width_slider = document.getElementById("width_slider");
const period_slider = document.getElementById("period_slider");
const sigma_slider = document.getElementById("sigma_slider");
// 3 график
const dft_button_walsh = document.getElementById("dft-button-walsh");
const sequency = document.getElementById("sequency_slider");
var number_plot;

// 1 график
setupSlider(frequency, out_frequency, 1);
setupSlider(freqsample, fs_out, 1);
setupSlider(chirp_freq, chirp_out, 1);
setupSlider(phase_signal, out_phase, 1);
setupButtons(buttons, 1);
setupDftButton(dft_button, 1)
// 2 график
setupButtons(buttons_imp, 2);
setupSlider(fs_imp, fs_imp_out, 2);
setupDftButton(dft_button_imp, 2);
setupSlider(phase_imp, out_phas_imp, 2);
setupSlider(width_slider, width_out, 2);
setupSlider(period_slider, period_out, 2);
setupSlider(sigma_slider, sigma_out, 2);
// 3 график
setupDftButton(dft_button_walsh, 3);
setupSlider(sequency_slider, out_sequency, 3);

// Кнопка Чирп
is_chirp.addEventListener('click', () => {
    document.getElementById("chirp-container").classList.toggle("active");
    updateValues(1);
});

// Настройка кнопки
function setupDftButton(name, number_plot) {
    name.addEventListener('click', () => {
    updateValues(number_plot);
    })
};

// Добавление кнопок
function setupButtons(elements, number_plot) {
    elements.forEach(button => {
        button.addEventListener('click', () => {
            if (button.classList.contains("selected")) {
                return;
            }
            // Убираем класс "selected" со всех кнопок
            elements.forEach(btn => btn.classList.remove('selected'));
            // Добавляем класс "selected" для нажатой кнопки
            button.classList.add('selected');

            if (button.value == "delta") {
                width_container.classList.remove("active");
                period_container.classList.remove("active");
                sigma_container.classList.remove("active");
            } else if (button.value == "square") {
                width_container.classList.add("active");
                sigma_container.classList.remove("active");
                period_container.classList.remove("active");
            } else if (button.value == "pulse_train" || button.value == "rand_pulse_train"){
                sigma_container.classList.remove("active");
                width_container.classList.add("active");
                period_container.classList.add("active");
            } else if (button.value == "gauss" || button.value == "exponent"){
                sigma_container.classList.add("active");
                width_container.classList.remove("active");
                period_container.classList.remove("active");}
            updateValues(number_plot);
        })
    })
};

//Добавить слайдбар
function setupSlider(element, out_element, number_plot) {
    // Вывод этого значения обратно на экран 
    out_element.innerHTML = element.value;
    element.addEventListener('input', function() {
        out_element.innerHTML = this.value;
        updateValues(number_plot);
    })
};


function updateValues(number_plot) {
    if (number_plot == 1)
        updatePlot({
            num_plot: 1,
            signal_type: document.querySelector(".type_signal.selected").value,
            is_dft: dft_button.checked,
            fs: parseInt(freqsample.value),
            phase: parseFloat(phase_signal.value),
            frequency: parseInt(frequency.value),
            is_chirp: is_chirp.checked,
            chirp_coef: parseInt(chirp_freq.value)
        })
    else if (number_plot == 2)
        updatePlot({
            num_plot: 2,
            signal_type: document.querySelector(".type_impuls.selected").value,
            is_dft: dft_button_imp.checked,
            fs: parseInt(fs_imp.value),
            phase: parseFloat(phase_imp.value),
            width: parseFloat(width_slider.value),
            period: parseFloat(period_slider.value),
            sigma: parseFloat(sigma_slider.value)
        })
    else if (number_plot == 3)
        updatePlot({
            fs: 128,
            num_plot: 3,
            sequency: parseInt(sequency.value),
            is_dft: dft_button_walsh.checked
        })
};

var layout_DFT = {
    xaxis: { title: {text: 'Частота, Гц', font: {color: 'white'}} },
    yaxis:{ title: {text: 'Время, с', font: {color: 'white'}} },
}; 

var layout_signal = {
    xaxis: { title: {text: 'Время, с', font: {color: 'white'}} },
    yaxis: { title: {text: 'Амплитуда', font: {color: 'white'}} },
}; 

var layout_init = {
    xaxis: { title: {text: 'Время, с', font: {color: 'white'}} },
    yaxis: { title: {text: 'Амплитуда', font: {color: 'white'}} },
    paper_bgcolor: '#444444',
    plot_bgcolor: '#c7c7c7',
    font: {color: 'white'},
    height: 350,
    margin: {l: 40, r: 20, t: 30, b: 40},
    padding: 0,
};

// Инициализация графика
function initPlot(data) {
    var trace = {
        x: data.time,
        y: data.signal,
        mode: 'lines',
        name: 'Signal',
        line: {color: '#522685', width: 2},
    };
    name_plot = 'plot' + data.num_plot
    Plotly.newPlot(name_plot, [trace], layout_init);
};

// Обновление графика
function updatePlot(params) {
    fetch('/plot_update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        let name_plot = 'plot' + params.num_plot;
        let update_data = {x: [data.time], y: [data.signal]};

        if (params.is_dft)
            Plotly.update(name_plot, update_data, layout_DFT);
        else
            Plotly.update(name_plot, update_data, layout_signal);
    })
    .catch(error => console.error("Error in graph draw", error))
};

// Функция инициализации
function initGraph(params) {
    fetch('/plot_update', {
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
    initGraph({num_plot: 1, frequency: 5});
    initGraph({num_plot: 2, signal_type: "delta"});
    initGraph({num_plot: 3, signal_type: "walsh", sequency: 10});
});

window.addEventListener('resize', function() {
    let container = document.querySelector('.graphcontainer');
    [1, 2, 3].forEach(num => Plotly.relayout('plot' + num, { width: container.clientWidth }));
});