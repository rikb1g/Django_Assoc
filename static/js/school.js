const btn_manage_school = document.getElementById('btn-manage-school')
const buttonsNav = document.querySelectorAll('.btn-nav-school')


buttonsNav.forEach(function(button){
 buttonsNav.forEach(function(btn){
        btn.classList.remove('btn-active')
       })
    })

console.log("funciona")
btn_manage_school.classList.add('btn-active')

// Função para obter o token CSRF
function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    cookies.forEach(cookie => {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            csrfToken = value;
        }
    });
    return csrfToken;
}
let currentActivityId = null; // Variável global para armazenar o ID da atividade

document.addEventListener('DOMContentLoaded', function () {
    // Adicionar um listener para todos os botões de edição de atividades
    document.querySelectorAll('.btn-edit-activity').forEach(button => {
        button.addEventListener('click', function () {
            currentActivityId = button.dataset.id; // Atualizar a variável com o ID correto da atividade

            
            fetch(`/school/edit_activity/${currentActivityId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro na resposta da requisição');
                    }
                    return response.json();
                })
                .then(data => {                
                        document.getElementById('Activityname').value = data.name;
                        document.getElementById('Activityvalue').value = data.value;
                   
                    
                })
                .catch(error => {
                    console.log('Erro ao buscar dados da atividade:', error);
                });
        });
    });

    // Submissão do formulário
    const formAtivities = document.getElementById('editActivityForm');
    formAtivities.addEventListener('submit', function (event) {
        event.preventDefault();

        if (!currentActivityId) {
            console.log('Erro: ID da atividade não definido');
            return;
        }

        const formData = new FormData(formAtivities);

        // Fazer a requisição POST para o endpoint correto com o ID da atividade
        fetch(`/school/edit_activity/${currentActivityId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('editActivitieModal'));
                modal.hide();
                alert('Atividade editada com sucesso');
                location.reload();
            } else {
                alert('Erro: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.log('Erro ao atualizar os dados da atividade:', error);
        });
    });
});

// form add activity


const formAddActivity = document.getElementById('insertActivityForm');

    formAddActivity.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(formAddActivity);

        fetch(`/school/addactivityform/`,{
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })

        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('insertActivitieModal'));
                modal.hide();
                alert('Atividade inserida com sucesso');
                location.reload();
            } else {
                alert('Erro: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.log('Erro ao inserir a atividade:', error);
        });

    })


// delete activity

function delete_activity(name, id) {
    if (confirm(`Deseja realmente excluir a atividade ${name}?`)) {
        fetch(`/school/delete_activity/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Atividade excluída com sucesso');
                location.reload();
            } else {
                alert('Erro: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.log('Erro ao excluir a atividade:', error);
        });
    }
}
