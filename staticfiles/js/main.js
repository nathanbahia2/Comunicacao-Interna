$(function () {
    $('[data-toggle="tooltip"]').tooltip();
})

$('input[type="date"]').each((i, el) => {
    if ($(el).attr('value')) {
        const value = $(el).attr('value');
        $(el).val(value.split('/').reverse().join('-'));
    } else {
        const hoje = new Date().toLocaleDateString();
        $(el).val(hoje.split('/').reverse().join('-'));
    }
});

const form_dias = $('#dias');
form_dias.on('change', function () {
    const dias = $(this).val();
    location.href = `${location.origin}${location.pathname}?dias=${dias}`;
});


const btn_finaliza_entrega = $('.btn-finaliza-entrega');
btn_finaliza_entrega.on('click', function () {
    const entrega = $(this).data('entrega');
    Swal.fire({
        title: 'Finalizar entrega',
        width: 800,
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Confirmar',
        reverseButtons: true,
        allowOutsideClick: false,
        html: `
            <div>
                <div class="form-group text-left mb-3">
                    <label for="recebimento_pedido">Data e hora do recebimento do pedido</label>
                    <input type="datetime-local" class='form-control' id='recebimento_pedido' name='recebimento_pedido' class='form-control'>
                </div>
                <div class="form-group text-left mb-3">
                    <label for="observacao_final">Observação final</label>
                    <textarea id='observacao_final' name='observacao_final' class='form-control' rows='3'></textarea>
                </div>
            </div>
        `
    }).then(result => {
        if (result.value) {
            const recebimento_pedido = $('#recebimento_pedido').val();
            const observacao_final = $('#observacao_final').val();

            $.post({
                url: '/entregas/finalizar/',
                data: {
                    entrega: entrega,
                    recebimento_pedido: recebimento_pedido,
                    observacao_final: observacao_final
                },
                success: function (data) {
                    if (data) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Entrega finalizada com sucesso'
                        }).then( () => { location.reload() })
                    }
                }
            });
        }
    });
});


const info_elogio = $('.btn-info-elogio');
info_elogio.on('click', function () {
    const elogio = $(this).data('elogio');
    $.get({
        url: '/elogios/info',
        data: {elogio: elogio},
        success: function (data)  {
            Swal.fire({
                icon: 'info',
                title: 'Informações do elogio',
                width: 800,
                html: `
                    <div class="text-left">
                        <b>Data</b>: ${data['data']} <br>
                        <b>Funcionário</b>: ${ data['funcionario'] } <br>
                        <b>Cargo</b>: ${ data['cargo'] } <br>
                        <b>Observação</b>: ${ data['observacao'] } <br>
                        <b>Cadastro</b>: ${ data['usuario'] } em ${ new Date(data['criacao']).toLocaleDateString() } <br>
                    </div>`
            });
        }
    });
});


const info_ocorrencia = $('.btn-info-ocorrencia');
info_ocorrencia.on('click', function () {
    const ocorrencia = $(this).data('ocorrencia');
    $.get({
        url: '/ocorrencias/info',
        data: {ocorrencia: ocorrencia},
        success: function (data)  {
            Swal.fire({
                icon: 'info',
                title: 'Informações da ocorrência',
                width: 800,
                html: `
                    <div class="text-left">
                        <b>Data</b>: ${data['data']} <br>
                        <b>Funcionário</b>: ${ data['funcionario'] } <br>
                        <b>Cargo</b>: ${ data['cargo'] } <br>
                        <b>Motivo</b>: ${ data['motivo'] } <br>
                        <b>Observação</b>: ${ data['observacao'] } <br>
                        <b>Cadastro</b>: ${ data['usuario'] } em ${ new Date(data['criacao']).toLocaleDateString() } <br>
                    </div>`
            });
        }
    });
});


const info_entrega = $('.btn-info-entrega');
info_entrega.on('click', function () {
    const entrega = $(this).data('entrega');
    $.get({
        url: '/entregas/entregas/info',
        data: {
            entrega: entrega
        },
        success: function (data)  {
            const status = data['recebida']
                ? {text: '<span class="text-success">Recebido</span>', icon: 'success'}
                : {text: '<span class="text-danger">Pendente</span>', icon: 'warning'}

            Swal.fire({
                icon: status['icon'],
                width: 800,
                html: `
                    <h2>Status: ${ status['text'] }</h2><hr>
                    <div class="text-left">
                        <div>
                            <b>Cliente</b>: ${data['cliente']} 
                            <b>Endereço</b>: ${data['endereco']}
                        </div>
                        <br>
                        <div>
                            <b>Pedido</b>: ${data['pedido']} 
                            <b>Valor</b>: ${data['valor']}
                        </div>
                        <br>
                        <div>
                            <b>Entregador</b>: ${data['entregador']} 
                            <b>Saída</b>: ${data['saida']}
                            <b>Recebimento</b>: ${data['recebimento']}
                        </div>
                        <br>
                        <b>Cadastro</b>: ${ data['cadastro'] }<br><br>
                        <b>Detalhes do pedido</b>: ${data['detalhes'] || '-----'}<br><br>
                        <b>Observação final</b>: ${data['observacao'] || '-----'}<br><br>
                    </div>`
            });
        }
    });
});


$('.btn-delete-elogio').on('click', function () {
    const button = $(this);
    const id = $(this).data("elogio");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir elogio",
        text: "Tem certeza que deseja excluir este elogio?",
        model: 'elogios',
        msgSuccess: "Elogio excluído com sucesso",
        msgError: "Falha ao excluir elogio"
    });
});


$('.btn-delete-ocorrencia').on('click', function () {
    const button = $(this);
    const id = $(this).data("ocorrencia");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir ocorrência",
        text: "Tem certeza que deseja excluir esta ocorrência?",
        model: 'ocorrencias',
        msgSuccess: "Ocorrência excluída com sucesso",
        msgError: "Falha ao excluir ocorrência"
    });
});


$('.btn-delete-email').on('click', function () {
    const button = $(this);
    const id = $(this).data("email");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir e-mail",
        text: "Tem certeza que deseja excluir este e-mail?",
        model: 'email',
        msgSuccess: "E-mail excluído com sucesso",
        msgError: "Falha ao excluir e-mail"
    });
});


$('.btn-delete-funcionario').on('click', function () {
    const button = $(this);
    const id = $(this).data("funcionario");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir funcionário",
        text: "Tem certeza que deseja excluir este funcionário?",
        model: 'funcionarios',
        msgSuccess: "Funcionário excluído com sucesso",
        msgError: "Falha ao excluir funcionário"
    });
});


$('.btn-delete-cargo').on('click', function () {
    const button = $(this);
    const id = $(this).data("cargo");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir cargo",
        text: "Tem certeza que deseja excluir este cargo?",
        model: 'cargos',
        msgSuccess: "Cargo excluído com sucesso",
        msgError: "Falha ao excluir cargo"
    });
});


$('.btn-delete-motivo').on('click', function () {
    const button = $(this);
    const id = $(this).data("motivo");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir motivo",
        text: "Tem certeza que deseja excluir este motivo?",
        model: 'motivos',
        msgSuccess: "Motivo excluído com sucesso",
        msgError: "Falha ao excluir motivo"
    });
});


$('.btn-delete-usuario').on('click', function () {
    const button = $(this);
    const id = $(this).data("usuario");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir usuário",
        text: "Tem certeza que deseja excluir este usuário?",
        model: 'usuarios',
        msgSuccess: "Usuário excluído com sucesso",
        msgError: "Falha ao excluir usuário"
    });
});


$('.btn-delete-entregador').on('click', function () {
    const button = $(this);
    const id = $(this).data("entregador");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir entregador",
        text: "Tem certeza que deseja excluir este entregador?",
        model: 'entregador',
        msgSuccess: "Entregador excluído com sucesso",
        msgError: "Falha ao excluir entregador"
    });
});


$('.btn-delete-entrega').on('click', function () {
    const button = $(this);
    const id = $(this).data("entrega");
    deleteObj({
        id: id,
        button: button,
        title: "Excluir entrega",
        text: "Tem certeza que deseja excluir esta entrega?",
        model: 'entrega',
        msgSuccess: "Entrega excluída com sucesso",
        msgError: "Falha ao excluir entrega"
    });
});


function deleteObj ({id, button, title, text, model, msgSuccess, msgError}) {
    const row = button.parent().parent().parent();
    Swal.fire({
        icon: 'question',
        title: title,
        text: text,
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Confirmar',
        reverseButtons: true
    }).then( result => {
        if (result.value) {
            $.post({
                url: "/delete/obj/",
                data: {
                    data: id,
                    model: model
                },
                success: function (response) {
                    if (response === true) {
                        Swal.fire({icon: 'success', title: msgSuccess}).then( () => { row.remove() });
                    } else {
                        Swal.fire({icon: 'error', title: msgError});
                    }
                },
            });
        }
    });
}