listQuestions = [];
quiz_atual = null; // mandar aqui o objeto do quiz atual se for editar

$(document).ready(function () {
    if (quiz_atual != null) {
        listQuestions = quiz_atual.questions;
        attributes.quiz_init(listQuestions);
    }else{
        attributes.quiz_init();
    }
});