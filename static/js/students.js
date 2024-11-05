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



document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-edit-student').forEach(button => {
        button.addEventListener('click', function () {
            const studentId = button.dataset.id;
            localStorage.setItem('studenID', studentId)

            // Faz a requisição fetch para buscar os dados do aluno
            fetch(`/student/student_update/${studentId}/`)
                .then(response => response.json())
                .then(data => {
                    const selectedActivity = data.activity;
                    const selectedFee = data.fee;

                    // Preenche os campos do formulário com os dados do aluno
                    document.getElementById('studentName').value = data.name;
                    document.getElementById('studentEntryYear').value = data.entry_year;
                    document.getElementById('studenteducationOfficer').value = data.education_officer;
                    document.getElementById('studentphoneNumeberOfficer').value = data.phone_numeber_officer;

                    // Limpa as opções previamente selecionadas no select de atividades
                    const activitySelect = document.getElementById('activitySelect');
                    activitySelect.innerHTML = '';
                    const feeSelect = document.getElementById('feeSelect');
                    feeSelect.innerHTML = '';

                    // Faz a requisição para buscar as mensalidades
                    fetch(`/student/all_fees/`)
                        .then(response => response.json())
                        .then(fees => {
                            fees.forEach(fee => {
                                const option = document.createElement('option');
                                option.value = fee.id;
                                option.textContent = fee.name;

                                if (selectedFee.includes(fee.id)) {
                                    option.selected = true;
                                }
                                feeSelect.appendChild(option);
                            });
                        })
                        .catch(error => {
                            console.log('Erro ao buscar as mensalidades:', error);
                        });

                    // Faz a requisição para buscar as atividades
                    fetch(`/school/all_activities/`)
                        .then(response => response.json())
                        .then(activities => {
                            activities.forEach(activity => {
                                const option = document.createElement('option');
                                option.value = activity.id;
                                option.textContent = activity.name;

                                if (selectedActivity.includes(activity.id)) {
                                    option.selected = true;
                                }
                                activitySelect.appendChild(option);
                            });
                        })
                        .catch(error => {
                            console.log('Erro ao buscar as atividades:', error);
                        });
                })
                .catch(error => {
                    console.log('Erro ao buscar os dados do aluno:', error);
                });
        });
    });

    const form = document.getElementById('editStudentForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

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

        const studentId = localStorage.getItem('studenID')
        const formData = new FormData(form);
        for (const [key, value] of formData.entries()) {
            if (value === '') {
                formData.delete(key);
            }
        }

        fetch(`/student/student_update/${studentId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editStudentModal'));
                    modal.hide();

                    alert('Aluno editado com sucesso');
                    location.reload();
                } else {
                    alert('Erro: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.log('Erro ao atualizar os dados do aluno:', error);
            });
    });
});


function deleteStudent(studentId, name) {
    if (confirm(`Tem certeza que deseja excluir o aluno ${name}?`)) {
        fetch(`/student/student_delete/${studentId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Aluno excluído com sucesso');
                    location.reload();
                } else {
                    alert('Erro: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.log('Erro ao excluir o aluno:', error);
            });
    }

}