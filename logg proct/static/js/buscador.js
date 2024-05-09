document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const dataTable = document.getElementById('dataTable');
    const tbody = dataTable.querySelector('tbody');

    searchInput.addEventListener('input', function () {
        const query = this.value;

        console.log(query);

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${query}`
        })
        .then(response => response.text()) // Recibir texto en lugar de JSON
        .then(data => {
            // Analizar la respuesta manualmente
            const parsedData = JSON.parse(data);

            tbody.innerHTML = '';

            parsedData.forEach(fila => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><img src="{{ url_for('static', filename='uploads/' + fila['img']) }}" alt="${fila['img']}"></td>
                    <td>${fila['descripcion']}</td>
                    <td>${fila['precio']}$</td>
                    <td>${fila['itbis']}%</td>
                    <td>${(fila['cantidad'] < 6) ? '<span class="red">' + fila['cantidad'] + '</span>' : fila['cantidad']}</td>
                    <td>
                        ${(fila['cantidad'] < 6) ? 
                            `<a href=""><button id="remove"><i class="fa-solid fa-triangle-exclamation"></button></i></a>`
                            : ''}
                        <a href="/edit/${fila['id']}"><button id="edit">Editar</button></a>
                        <a href="/remove_art/${fila['id']}"><button id="remove" class="Borrar" value="${fila['id']}">Borrar</button></a>
                    </td>`;
                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error:', error));
    });
});