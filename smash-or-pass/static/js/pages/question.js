
function delQuestion(button_click) {
    div_question = button_click.parentNode;
    //get input id from question_id
    id = div_question.querySelector('input[name="question_id"]').value;
    $.ajax({
        url: 'url de deletar o personagem kkk',
        method: 'POST',
        data: {
            id
        },
        dataType: 'json',
        success: function (response) {
            responde = response.json(); // caso venha dentro de outra var colocar .response
            if (responde.status == 'success') {
                div_question.remove();
            }
        },
        error: function (error) {
            const return_alert = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            });
            return_alert.fire({
                icon: 'danger',
                title: error.responseJSON.message,
            });
        }
    });
}
$('#question_cadastrar').on('click', function () {
    $.ajax({
        url: 'url de cadastrar o personagem kkk',
        method: 'POST',
        data: {
            name: $('#question_name').val(),
            image: $('#question_image').val(),
            attributes: $('#attributes_list').val(),
            quiz_id: quiz_atual.id
        },
        dataType: 'json',
        success: function (response) {
            response = response.data; // caso venha dentro de outra var colocar .response

            $listaCadastrados = document.querySelector('#lista_cadastrados');

            for (const question of response) {
                const $listItem = document.createElement("div");

                listaCadastrados.classList.add('col-md-4 col-sm-6 text-center position-relative question-div');

                var $name_char = document.createElement('p');
                $name_char.textContent = question.name;
                $name_char.classList.add('text-muted');

                $listItem.appendChild($name_char);

                var $image_char = document.createElement('img');
                $image_char.src = question.image;
                $image_char.classList.add('img-fluid');

                $listItem.appendChild($image_char);

                var $button_exclude = document.createElement('button');
                $button_exclude.classList.add('close');
                $button_exclude.type = 'button';
                var $ico_exlude = document.createElement('span');
                $ico_exlude.setAttribute('aria-hidden', 'true');
                $ico_exlude.innerHTML = '&times;';
                $button_exclude.createElement($ico_exlude);
                $button_exclude.setAttribute('onClick', 'delQuestion(this)');

                $listItem.appendChild($image_char);

                var $input_hidden = document.createElement('input');
                $input_hidden.type = 'hidden';
                $input_hidden.id = 'question_id';
                $input_hidden.name = 'question_id';
                $input_hidden.value = question.id;

                $listItem.appendChild($input_hidden);

                $listaCadastrados.appendChild($listItem);
            }
        },
        error: function (xhr, status, error) {
            Swal.fire({
                title: 'Erro ao cadastrar!',
                text: error.responseJSON.message,
                icon: 'danger',
                confirmButtonText: 'Ok'
            });
        }
    });

});

$('#question_image').on('change', function () {
    $('#question_image_preview').attr('src', $(this).val());
    $('#question_image_preview').slideToggle();
});