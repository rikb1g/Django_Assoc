const btn_manage_school = document.getElementById('btn-manage-school')
const buttonsNav = document.querySelectorAll('.btn-nav-school')


buttonsNav.forEach(function (button) {
    buttonsNav.forEach(function (btn) {
        btn.classList.remove('btn-active')
    })
})


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

    // TYpe FEE update form

    document.querySelectorAll('.btn-update-fee').forEach(button => {
        button.addEventListener('click', function () {
            currentFeeID = button.dataset.id; 

            fetch(`/student/update_type_fee/${currentFeeID}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta da requisição');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('FeenameUp').value = data.name;
                document.getElementById('FeevalueUp').value = data.value;
            })
            .catch(error => {
                console.log('Erro ao buscar dados da mensalidade:', error);
            });



        });

        const formTypeFee = document.getElementById('updateFeeForm');
        formTypeFee.addEventListener('submit', function (event) {
            event.preventDefault();
            
            if (!currentFeeID) {
                console.log('Erro: ID da atividade não definido');
                return;
            }
            
    
            const formData = new FormData(formTypeFee);
    
            // Fazer a requisição POST para o endpoint correto com o ID da atividade
            fetch(`/student/update_type_fee/${currentFeeID}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('updateFeeModal'));
                        modal.hide();
                        alert('Mensalidade editada com sucesso');
                        location.reload();
                    } else {
                        alert('Erro: ' + JSON.stringify(data.errors));
                    }
                })
                .catch(error => {
                    console.log('Erro ao atualizar os dados da mensalidade:', error);
                });
        });


    });

    
});

// form add


// add activity


const formAddActivity = document.getElementById('insertActivityForm');

formAddActivity.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(formAddActivity);

    fetch(`/school/addactivityform/`, {
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

// add teacher form
document.addEventListener('DOMContentLoaded', function () {
    const modalElement = document.getElementById('addTeacherModal');

    // Carregar atividades quando o modal for exibido
    modalElement.addEventListener('shown.bs.modal', function () {
        const activitySelectTeacher = document.getElementById('activitySelectTeacher');
        activitySelectTeacher.innerHTML = '';

        fetch(`/school/all_activities/`)
            .then(response => response.json())
            .then(activities => {
                activities.forEach(activity => {
                    const option = document.createElement('option');
                    option.value = activity.id;
                    option.textContent = activity.name;
                    activitySelectTeacher.appendChild(option);
                });
            })
            .catch(error => {
                console.log('Erro ao buscar as atividades:', error);
            });
    });

    // Submissão do formulário form add
    const formAddTeacher = document.getElementById('insetTeacherForm');
    formAddTeacher.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(formAddTeacher);

        fetch(`/school/addTeacherForm/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addTeacherModal'));
                    modal.hide();
                    alert('Professor inserido com sucesso');
                    location.reload();
                } else {
                    alert('Erro: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.log('Erro ao inserir o professor:', error);
            });
    });

    // update teacher form

    document.querySelectorAll('.btn-updtate-teacher').forEach(button => {
        button.addEventListener('click', function () {
            const teacherId = button.dataset.id;
            fetch(`/school/update_teacher/${teacherId}/`)
                .then(response => response.json())
                .then(data => {
                    const selectAtivityTeacher = data.activity
                    console.log(data)
                    document.getElementById('TeacherNameUP').value = data.name;
                    document.getElementById('TeacherPhoneUP').value = data.phone;
                    document.getElementById('TeacherEmailUP').value = data.email;
                    document.getElementById('TeacherClassScheduleUP').value = data.class_schedule



                    const activitySelectTeacherUP = document.getElementById('activitySelectTeacherUpdate');
                    activitySelectTeacherUP.innerHTML = '';

                    fetch(`/school/all_activities/`)
                        .then(response => response.json())
                        .then(activities => {

                            activities.forEach(activity => {
                                console.log(activity)

                                const option = document.createElement('option');
                                option.value = activity.id;
                                option.textContent = activity.name;

                                activitySelectTeacherUP.appendChild(option);

                                if(activity.id == selectAtivityTeacher){
                                    option.selected = true;
                                }


                            })
                        }).catch(error => {
                            console.log('Erro ao buscar as atividades:', error);
                        });
                })
                .catch(error => {
                    console.log('Erro ao buscar os dados do professor:', error);
                });




        });
    });

    // submit update teacher form

    const updateTeacherForm = document.getElementById('updateTeacherForm');
    updateTeacherForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const teacherId = document.querySelector('.btn-updtate-teacher').dataset.id

        const dataForm = new FormData(updateTeacherForm);

        fetch(`/school/update_teacher/${teacherId}/`, {
            method: 'POST',
            body: dataForm,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('updateTeacherModal'));
                    modal.hide();
                    alert('Professor atualizado com sucesso');
                    location.reload();
                } else {
                    alert('Erro: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.log('Erro ao atualizar o professor:', error);
            });
    });


});

// update teacher form


// Delete teacher
function delete_teacher(name, id) {
    if (confirm(`Deseja realmente excluir o professor ${name}?`)) {
        fetch(`/school/delete_teacher/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Professor excluído com sucesso');
                    location.reload();
                } else {
                    alert('Erro: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.log('Erro ao excluir o professor:', error);
            });
    }
}




// submit type form
const formAddTypeFee = document.getElementById('insertFeeForm');
formAddTypeFee.addEventListener('submit', function (event) {
    event.preventDefault(); 

    const formData = new FormData(formAddTypeFee);

    fetch(`/student/add_fee_form/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('insertFeeModal'));
                    modal.hide();
                alert('Mensalidade inserida com sucesso');
                location.reload();
            } else {
                alert('Erro: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.log('Erro ao inserir a mensalidade:', error);
        });

})

function delete_fee_type(name, id) {    
    if (confirm(`Deseja realmente excluir a Mensalidade ${name}?`)) {
        fetch(`/student/delete_type_fee_form/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Mensalidade excluída com sucesso');
                    location.reload();
                } else {
                    alert('Erro: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.log('Erro ao excluir a Mensalidade:', error);
            });
    }
}
