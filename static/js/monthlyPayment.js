function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showFees(selectedMonth){
    const rows = document.querySelectorAll("#tableMontlyPayments")

    rows.forEach(row => {
        const rowMonth = row.getAttribute("data-month")

        if (selectedMonth === "" || rowMonth === selectedMonth){
            row.style.display = "";
        }else {
            row.style.display = 'none'
        }
    })
}


document.getElementById('filterMonth').addEventListener("change", function(){
    const selectedMonth = this.value

    showFees(selectedMonth)
    

    
})

const currentDate = new Date();
    const months = [
        "January", "February", "March", "April", "May", "June", "July", 
        "August", "September", "October", "November", "December"
    ];
    
    const currentMonth = months[currentDate.getMonth()];
    const currentYear = currentDate.getFullYear();

    // Formatar o valor no formato esperado, ex: "October 2024"
    const currentMonthYear = `${currentMonth} ${currentYear}`;
    console.log(currentMonthYear)

    // Selecionar o <select> e definir a opção correta como selecionada
    const filterMonthSelect = document.getElementById("filterMonth");
    for (const option of filterMonthSelect.options) {
        if (option.value === currentMonthYear) {
            console.log(option.value)
            option.selected = true;
            showFees(currentMonthYear)
            break;
        }
    }



function checkfee(mensalidadeID){

    const studentValue = document.getElementById(`studentValue_${mensalidadeID}`)

    if (isNaN(studentValue.value) || studentValue.value.trim() === "" ){
        alert("Por favor, insira um valor válido")
    }

    fetch(`/student/insert_fee/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id:mensalidadeID,
            value: studentValue.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){           
            alert("Mensalidade atualizada com sucesso")
            location.reload();
            
        }else {
            alert("Erro ao atualizar mensalidade")
        }
    })
    .catch((error)=>{
        console.error('Error', error)
    })
}


function exitUpdateFee(mensalidadeID){
    fetch(`/student/remove_fee/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id:mensalidadeID
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            alert("Mensalidade atualizada com sucesso")
            location.reload()
        } 
        else{
            alert("Erro ao atualizar a mensalidade")
        }
    })
    .catch((error)=> {
        console.error('Error', error)
    })
}
function uptdateFee(mensalidadeID) {
    // Selecione o `<td>` que contém o valor
    const studentValueTd = document.getElementById(`studentValueP_${mensalidadeID}`);
    const imageTd = document.getElementById(`imageTdOPe_${mensalidadeID}`)

    if (studentValueTd) {
        
        const currentValue = studentValueTd.innerText.trim();

        // Limpe o conteúdo do `<td>`
        studentValueTd.innerHTML = '';

        // Crie o campo de entrada `<input>` para edição
        const inputValue = document.createElement('input');
        inputValue.type = 'text';
        inputValue.className = 'form-control-sm';
        inputValue.id = `studentValue_${mensalidadeID}`
        inputValue.value = currentValue;  // Defina o valor inicial do input

        // Adicione o `<input>` dentro do `<td>`
        studentValueTd.appendChild(inputValue);

        // change image
        imageTd.innerHTML = ''
        const image_saveA = document.createElement('a')
        const image_save = document.createElement('img')
        
        
        image_save.src = checkImageUrl
        image_save.onclick = function(){ checkfee(mensalidadeID)}
        image_save.alt = 'Guardar'
        image_saveA.appendChild(image_save)
        imageTd.appendChild(image_saveA)

        // close buttom
        const image_closeA = document.createElement('a')
        const image_close = document.createElement('img')
        image_close.src = closeImageUrl
        image_close.alt = "Anular"
        image_close.onclick = function(){exitUpdateFee(mensalidadeID)} 

        
        image_closeA.appendChild(image_close)
        imageTd.appendChild(image_closeA)
        

    }
}
