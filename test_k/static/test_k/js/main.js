
$('#btn-cargar').on('click', function () {
    var form = document.getElementById("form-cargar-file");
    var fd = new FormData(form);
    csrftoken = getCookie('csrftoken');
    fd.append("csrfmiddlewaretoken", csrftoken);
    const response = axios.post('/test/cargar-datos/', fd,).then(res => {

        if (response) {
            iziToast.success({
                timeout: 4000,
                title: 'Éxito',
                position: 'center',
                message: 'Los datos se cargaron correctamente',
            });
        }


    }).catch((err) => {
        iziToast.error({
            timeout: 4000,
            title: 'Error',
            position: 'center',
            message: 'Ocurrio un error.' + err,
        });
    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


