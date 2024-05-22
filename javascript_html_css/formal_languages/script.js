const lectures = [{
        title: 'Лекция 1',
        file: 'first_lection.html'
    },
    {
        title: 'Лекция 2',
        file: 'second_lection.html'
    },
    {
        title: 'Лекция 3',
        file: 'third_lection.html'
    },
    {
        title: 'Лекция 4',
        file: 'fourth_lection.html'
    },
    {
        title: 'Лекция 5',
        file: 'fifth_kection.html'
    },
    {
        title: 'Лекция 6',
        file: 'sixth_lection.html'
    },
    {
        title: 'Практика 1',
        file: 'first_practic.html'
    },
    {
        title: 'Практика 2',
        file: 'second_practic.html'
    },
    {
        title: 'Практика 3',
        file: 'third_practic.html'
    },
    {
        title: 'Практика 4',
        file: 'fourth_practic.html'
    },
    {
        title: 'Практика 5',
        file: 'fifth_practic.html'
    },
    {
        title: 'Практика 6',
        file: 'sixth_practic.html'
    },
];

const lecturesContainer = document.getElementById('lectures-container');

lectures.forEach(lecture => {
    const lectureBlock = document.createElement('div');
    lectureBlock.classList.add('lecture-block');

    const button = document.createElement('button');
    button.classList.add('lecture-button');
    button.textContent = lecture.title;

    const productDiv = document.createElement('div');
    productDiv.classList.add('flex', 'min-h-screen', 'items-center', 'justify-center');

    const productContent = `
    <div class="max-w-xs cursor-pointer rounded-xl p-2 shadow duration-150 hover:scale-105 hover:shadow-md flex flex-col items-center justify-center min-h-[200px]">
            <a target="_blank" href="lections/${lecture.file}">
              <button class="px-32 py-20 rounded-lg text-center bg-[#333333] text-white font-bold text-3xl hover:bg-white hover:text-[#191919] transition duration-300 ease-in-out whitespace-nowrap overflow-hidden text-ellipsis">
                <p class="text-center">${lecture.title}</p>
              </button>
            </a>
          </div>`;

    button.addEventListener('click', function () {
        fetch(`lections/${lecture.file}`)
            .then(response => response.text())
            .then(lectureContent => {
                const lectureWindow = window.open();
                lectureWindow.document.write(`
                <!DOCTYPE html>
                    <html>
                        <head>
                            <title>${lecture.title} | formal_languages</title>
                            <link rel="stylesheet" href="output.css">
                            <link rel="shortcut icon" href="img/unnamed.png" type="image/x-icon">
                            <link rel="stylesheet" type="text/css" href="lections/third_lection.css">
                        </head>
                        <body class="bg-[#292c4d]">
                        <div class="space-y-10">
                            <h1 class="text-center text-5xl text-white font-bold">${lecture.title}</h1>
                            <div class="lecture-content bg-[#414578] text-white font-medium">${lectureContent}</div>
                        </div> 
                        </body>
                        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
                    </html>
                `);
            })
            .catch(error => console.error('Ошибка при загрузке лекции:', error));
    });

    productDiv.innerHTML = productContent;
    productDiv.appendChild(lectureBlock);
    lecturesContainer.appendChild(productDiv);
});