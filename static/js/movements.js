


function applyFilterTabe(selectedMonth){
    const rowsFees = document.querySelectorAll('.table-Fees-Movements')
    const rowsMovements = document.querySelectorAll('.table-Income')
    const rowsExpenses = document.querySelectorAll('.table-expense')

    rowsFees.forEach(row => {
        const rowMonth = row.getAttribute("data-month")
        console.log(rowMonth)

        if (selectedMonth === "" || rowMonth.includes( selectedMonth)){
            row.style.display = "";
        }else{
            row.style.display = 'none'
        }
    })
    rowsMovements.forEach(row => {
        const rowMonth = row.getAttribute("data-month")

        if (selectedMonth === "" || rowMonth.includes(selectedMonth)){
            row.style.display = "";
        }else{
            row.style.display = 'none'
        }
    })
    rowsExpenses.forEach(row => {
        const rowMonth = row.getAttribute("data-month")
        console.log(rowMonth)

        if (selectedMonth === "" || rowMonth.includes( selectedMonth)){
            row.style.display = "";
        }else{
            row.style.display = 'none'
        }
    })
}



document.getElementById('filterMonth').addEventListener("change", function(){
    const selectedMonth = this.value
    console.log(selectedMonth)

    applyFilterTabe(selectedMonth)
    

    
})


const currentDate = new Date();
    const months = [
        "January", "February", "March", "April", "May", "June", "July", 
        "August", "September", "October", "November", "December"
    ];
    
const currentMonth = months[currentDate.getMonth()];
const currentYear = currentDate.getFullYear();

const currentMonthYear = `${currentMonth} ${currentYear}`;
console.log(currentMonthYear)
    

    // Selecionar o <select> e definir a opção correta como selecionada
const filterMonthSelect = document.getElementById("filterMonth");
for (const option of filterMonthSelect.options) {
    if (option.value === currentMonthYear) {
        console.log(option.value)
        option.selected = true;
        applyFilterTabe(currentMonthYear)
        break;
        }
    }


function deleteMovement(id, description){
    if (confirm(`Tem certeza que deseja excluir o movimento "${description}"?`)) {
        console.log(`/financeManagment/delete_movements/${id}`)
        window.location.href = `/finance/delete_movements/${id}/`;
    }
}