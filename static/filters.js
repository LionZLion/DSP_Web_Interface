// График 1
const sigmaSlider = document.getElementById("sigma_slider");
const dft_noise = document.getElementById("dft-noise");
const buttons_noise = document.querySelectorAll(".type_noise");
// График 2
const order_slider = document.getElementById("order_slider");
const cut_of_right_slider = document.getElementById("cut_of_right_slider");
const cut_of_left_slider = document.getElementById("cut_of_left_slider");
const type_impulse = document.querySelectorAll(".type_impulse");
const type_iir = document.querySelectorAll(".type_iir");
const type_window = document.querySelectorAll(".type_window");
const regime_filter = document.querySelectorAll(".regime_filter");
const order_slider_iir = document.getElementById("order_slider_iir");
var number_plot;
// График 3
const frequency = document.getElementById("frequency_slider");
const chirp_freq = document.getElementById("chirp_slider");
const buttons = document.querySelectorAll(".type_signal");
const is_chirp = document.getElementById("chirp-button");
const dft_button = document.getElementById("dft-button");
const phase_signal = document.getElementById("phase_signal");
const sigma_slider_filter = document.getElementById("sigma_slider_filter");
const dft_button_signal = document.getElementById("dft-button-signal");
const type_noise_signal = document.querySelectorAll(".type_noise_signal");

// График 1
setupSlider(sigmaSlider, sigma_out, 4);
setupDftButton(dft_noise, 4);
setupButtons(buttons_noise, 4);
// График 2
setupButtons(type_impulse, 5);
setupButtons(type_iir, 5);
setupButtons(type_window, 5);
setupButtons(regime_filter, 5);
setupSlider(order_slider, order_out, 5);
setupSlider(order_slider_iir, order_out_iir, 5);
setupSlider(cut_of_right_slider, cut_of_right_out, 5);
setupSlider(cut_of_left_slider, cut_of_left_out, 5);
// График 3
setupSlider(frequency, out_frequency, 6);
setupSlider(chirp_freq, chirp_out, 6);
setupSlider(phase_signal, out_phase, 6);
setupButtons(buttons, 6);
setupDftButton(dft_button_signal, 6);
setupButtons(type_noise_signal, 6);
setupSlider(sigma_slider_filter, sigma_out_filter, 6);


is_chirp.addEventListener('click', () => {
    document.getElementById("chirp-container").classList.toggle("active");
    updateValues(6);
});


// Настройка кнопки
function setupDftButton(name, number_plot) {
    name.addEventListener('click', () => { updateValues(number_plot) })
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

            if (button.value == "iir"){
                document.getElementById("type_filter-container").classList.add("active");
                document.getElementById("order_slider_iir-container").classList.add("active");
                document.getElementById("type_window-container").classList.remove("active");
                document.getElementById("order_slider_fir-container").classList.remove("active");
            }
            else if (button.value == "fir"){
                document.getElementById("order_slider_fir-container").classList.add("active");
                document.getElementById("type_filter-container").classList.remove("active");
                document.getElementById("type_window-container").classList.add("active");
                document.getElementById("order_slider_iir-container").classList.remove("active");
            }
            else if (button.value == "bandpass" || button.value == "bandstop"){
                document.getElementById("regime_left-container").classList.add("active");
                document.getElementById("regime_right-container").classList.add("active");
            }
            else if (button.value == "lowpass"){
                document.getElementById("regime_left-container").classList.remove("active");
                document.getElementById("regime_right-container").classList.add("active");
            }
            else if (button.value == "highpass"){
                document.getElementById("regime_right-container").classList.remove("active");
                document.getElementById("regime_left-container").classList.add("active");
            }
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


var layout_filter = {
    yaxis: { 
        title: {
            text: 'Амплитуда, Дб',
            font:  {color: 'rgb(162, 133, 189)'},
        },
        tickfont: {color: 'rgb(162, 133, 189)'}
    },
    yaxis2: {
        title: {
            text: 'Фазовый сдвиг, рад',
            font: {color: '#7dcbb2'},
        },
        tickfont: {color: '#7dcbb2'},
        overlaying: 'y',
        side: 'right'
    },
    xaxis: { 
        title: {
            text: 'Частота, Гц',
            font: {color: 'white'},
        },
    },
    paper_bgcolor: '#444444',
    plot_bgcolor: '#c7c7c7',
    font: {color: 'white'},
    height: 400,
    margin: {l: 50, r: 50, t: 30, b: 40},
    padding: 0 ,
    showlegend: false,
};

var layout_DFT = {
    xaxis: { title: {text: 'Частота, Гц', font: {color: 'white'}} },
    yaxis:{ title: {text: 'Амплитуда', font: {color: 'white'}} },
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
    height: 400,
    margin: {l: 50, r: 20, t: 30, b: 40},
    padding: 0,
    legend: {
        orientation: 'h',
        x: 0.5,
        y: -0.2, 
        xanchor: 'center',
        yanchor: 'top',
    },
};

function trace_signal(data) {
    let trace_data = [{
        x: (data.num_plot == 5) ? data.freq : data.time,
        y: (data.num_plot == 5) ? data.h_db : data.signal,
        mode: 'lines',
        name: 'Сигнал',
        line: {color: '#522685', width: 2},
        secondary_y: (data.num_plot == 5) ? true : false,
    }];
    return trace_data
}
// Инициализация графика


function updateValues(number_plot) {
    if (number_plot == 4)
        updatePlot({
            num_plot: number_plot,
            fs: 400,
            is_dft: dft_noise.checked,
            sigma: parseFloat(sigmaSlider.value),
            signal_type: document.querySelector(".type_noise.selected").value,
        })
    else {
        let type_imp = document.querySelector(".type_impulse.selected").value;
        updatePlot({
            num_plot: number_plot,
            type_iir: document.querySelector(".type_iir.selected").value,
            order: (type_imp == 'fir') ? parseInt(order_slider.value) : parseInt(order_slider_iir.value),
            cut_of_right: parseInt(cut_of_right_slider.value),
            cut_of_left: parseInt(cut_of_left_slider.value),
            type_window: document.querySelector(".type_window.selected").value,
            type_impulse: type_imp,
            regime_filter: document.querySelector(".regime_filter.selected").value,
            frequency: parseInt(frequency.value),
            is_chirp: is_chirp.checked,
            chirp_coef: parseInt(chirp_freq.value),
            phase: parseFloat(phase_signal.value),
            sigma: parseFloat(sigma_slider_filter.value),
            is_dft: dft_button_signal.checked,
            signal_type: document.querySelector(".type_signal.selected").value,
            noise_type: document.querySelector(".type_noise_signal.selected").value,
        })
        
    }
};

// Обновление графика
function updatePlot(params) {
    fetch('/plot_update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        let num = params.num_plot;
        let name_plot = 'plot' + num;
        if (num > 4){
            for (num; num <= 6; num++){
                data.num_plot = num
                name_plot = 'plot' + num;
                let update_data = trace_signal(data);
                var layout = layout_init;
                if (num == 5){
                    update_data.push({
                        x: data.freq, 
                        y: data.phase, 
                        name: 'phase response', 
                        yaxis: 'y2', 
                        line: {color: '#6fa392', width: 2, dash: 'dash'} 
                    });
                    layout = layout_filter;
                }
                else {
                    update_data.push({
                        x: data.time, 
                        y: data.filtred_signal, 
                        name: 'Фильтрованный сигнал', 
                        line: {color: '#fca503', width: 2} 
                    });
                };
                Plotly.newPlot(name_plot, update_data, layout);
                if (num == 6){
                    layout = (params.is_dft) ? layout_DFT : layout_signal;
                    Plotly.update(name_plot, update_data, layout);
                }
        }}
        else{
            layout = params.is_dft ? layout_DFT : layout_signal;
            let update_data = {x: [data.time],y: [data.signal]};
            Plotly.update(name_plot, update_data, layout);
        }
    })
    .catch(error => console.error("Error in graph draw", error))
};

// Инициализация
function initPlot(data) {
    let num_plot = data.num_plot;
    let name_plot = 'plot' + num_plot
    let trace_data = trace_signal(data);
    
    if (data.num_plot == 5) {
        trace_data.push({
            x: data.freq, 
            y: data.phase, 
            name: 'phase response', 
            yaxis: 'y2', 
            line: {color: '#6fa392', width: 2, dash: 'dash'} 
        });
    }
    else if (data.num_plot == 6) {
        trace_data.push({
            x: data.time, 
            y: data.filtred_signal, 
            name: 'Фильтрованный сигнал', 
            line: {color: '#fca503', width: 2},
        })
    }

    Plotly.newPlot(name_plot, trace_data, (data.num_plot == 5) ? layout_filter : layout_init);
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
};

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
    initGraph({ num_plot: 4, signal_type: 'white', sigma: 0.1 });
    initGraph({ num_plot: 5 });
    initGraph({ num_plot: 6 });
});

window.addEventListener('resize', () => {
    const container = document.querySelector('.graphcontainer');
    [4, 5, 6].forEach(num => Plotly.relayout('plot' + num, { width: container.clientWidth }));
});