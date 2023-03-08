$('body').append(`
    <input type="hidden" id="attributes_list" name="attributes_list" value="[]">
`);

input_attributes = document.querySelector('#attributes_list');


/**
 * atributes: {
 *  name: string,
 *  type: string,
 *  value: string
 * }
 */

attributes = {
    list: [],
    list_use: [],
    change: function () {
        //remove use param
        list_clear = [];
        for (const attribute of attributes.list) {
            list_clear.push({
                name: attribute.name,
                type: attribute.type,
                value: attribute.value
            });
        }
        input_attributes.value = JSON.stringify(list_clear);
    },
    quiz_init : function (questions=0) {
        if(questions == 0){
            $('#use_attributes').css('display','none');
            attributes.table.table_use_visible = true;
        }else{
            for (const question of questions) {
                for (const attribute of question.attributes) {
                    attributes.add_all(attribute.name, attribute.type, attribute.value);
                }
            }
        }
    },
    add_all: function (name, type, value) {
        //check if attribute is in list
        for (const attribute of attributes.list) {
            if(attribute.name == name){
                return;
            }
        }
        attributes.list.push({
            name: name,
            type: type,
            value: value,
            use: false
        });
    },
    add_new: function (name, type, value) {
        attributes.add_all(name, type, value);
        attributes.list_use.push({
            name: name,
            type: type,
            value: value
        });
        attributes.change();
    },
    remove: function (name) {
        attributes.list_use = attributes.list_use.filter(function (attribute) {
            return attribute.name != name;
        });
    },
    not_use_all: function () {
        for (const attribute of attributes.list) {
            attribute.use = false;
        }
        attributes.list_use = [];
    },
    get: function (use_list) {
        for(const attribute of use_list){
            attributes.use(attribute.name, attribute.type, attribute.value);
            //search in list to is attribute and set use true
            for (const attribute_list of attributes.list) {
                if(attribute_list.name == attribute.name){
                    attribute_list.use = true;
                    break;
                }
            }
        }
    },
}

attributes.table = {
    table_use_visible: false,
    print: function (attribute, click_to_add=false) {
        del = `<td>
            <button type="button" class="btn btn-danger" onClick="attributes.table.minus('#attr_${attribute.name}')">Remover</button>
        </td>`;
        if(click_to_add == false){
            del = '';
        }

        return `
        <tr id="attr_${attribute.name}"  ${click_to_add ? 'onClick="attributes.table.add(\''+attribute.name+'\', \''+attribute.type+'\', \''+attribute.value+'\')"' : ''}>
            <td>${attribute.name}</td>
            <td>${attribute.type}</td>
            <td>${attribute.value}</td>
            ${del}
        </tr>
        `;
    },
    add: function (name, type, value) {
        attributes.add_new(name, type, value);
        if (attributes.table.table_use_visible == true) {
            $('#use_attributes').slideDown();
        }
        attributes.ui.reset();
    },
    minus: function (tr_id) {
        tr = $(tr_id);
        attributes_name = $(tr).children()[0].innerHTML;
        attributes_type = $(tr).children()[1].innerHTML;
        attributes_value = $(tr).children()[2].innerHTML;

        attributes.remove(attributes_name);

        attributes.change();
    },
    refresh: function () {
        all = '';
        use = '';

        $table_use = $('#table_use_attribute');
        $table_all = $('#table_all_attribute');
        
        $($table_use).html(use);
        $($table_all).html(all);

        for (const attribute of attributes.list) {
            if(attribute.use){
                all += attributes.table.print(attribute, false);
            }else{
                use += attributes.table.print(attribute, true);
            }
        }
        //clear all tables
        $($table_use).html(use);
        $($table_all).html(all);
    },
}
attributes.ui = {
    new: function (name, type, value) {
        name = name.toLowerCase();
        //capitalize first letter
        name = name.charAt(0).toUpperCase() + name.slice(1);

        if(name == '' || type == '' || value == '' || type == 'Escolha...'){
            return false;
        }

        for (const attribute of attributes.list) {
            if(attribute.name == name){
                return false;
            }
        }

        attributes.table.add(name, type, value);

        attributes.ui.reset();

        return true;
    },
    reset: function () {
        $('#attribute_name').val('');
        $('#attribute_type').val('');
        $('#attribute_value').val('');

        attributes.change();

        attributes.table.refresh();
    }
}

$('#button_attribute').on('click', function () {
    deu_certo = attributes.ui.new($('#attribute_name').val(), $('#attribute_type').val(), $('#attribute_value').val());
    if(!deu_certo){
        Swal.fire({
            title: 'Erro',
            text: 'Atributo já cadastrado, ou parâmetros inválidos!',
            icon: 'error',
            confirmButtonText: 'Ok'
        });
    }
});

$('#button_reset_use_attribute').on('click', function () {
    attributes.not_use_all();
    attributes.ui.reset();
});

$('#type_attribute').on('change', function () {
    if($(this).val() == 'porcent'){
        $('#explicao_burra').html(`
            <small> No final, usaremos um valor para calcular a aprovação de um atributo, somando todos os seus valores.. </small>
            `);
    }
    if($(this).val() == 'boolean'){
        $('#explicao_burra').html(`
            <small> Ao final do quiz, esse valor será convertido em um ponto unitário no cálculo comparativo geral. </small>
        `);
    }
});